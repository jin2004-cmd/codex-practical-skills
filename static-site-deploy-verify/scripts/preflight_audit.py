#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态站发布前三轮体检（preflight）

用法:
    python preflight_audit.py --root ./site            # 三轮全跑
    python preflight_audit.py --root ./site --no-net   # 跳过外链联网测试（离线/内网）
    python preflight_audit.py --root ./site --json     # 机器可读输出

第一轮 链接：本地相对链接存在性 / 大小写一致 / 本地绝对路径泄漏 / 外链直连可达（绕开本机代理）
第二轮 结构：标签配平 / 重复 id / 锚点目标 / 图片 alt / title+viewport / 内联 JS 语法 / rel=noopener
第三轮 内容：同一指标多值冲突 / 占位符残留

退出码：0 = 无阻断问题；1 = 有阻断问题（死链、大小写、JS 语法、绝对路径）
"""
import argparse, json, os, re, ssl, subprocess, sys, tempfile, time
import urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
ATTR = re.compile(r'(?:href|src|data-poster|poster)\s*=\s*["\']([^"\']+)["\']')
ABS_LEAK = re.compile(r'(?:href|src)\s*=\s*["\'](?:file:|[A-Za-z]:[\\/])', re.I)
# type="application/ld+json" / 带 src 的外链脚本都不是内联 JS
SCRIPT = re.compile(r'''<script(?![^>]*ld\+json)(?![^>]*\bsrc=)[^>]*>(.*?)</script>''', re.S | re.I)
SKIP_SCHEME = ("http", "#", "data:", "mailto:", "javascript:", "tel:")

# 常见的指标句式；按需增删
METRIC_PROBES = {
    "作品页数": r"(?<!\d)(\d{1,3})\s*个作品页",
    "工具数": r"(?<!\d)(\d{1,3})\s*个(?:可直接试用的)?工具",
    "文档数": r"(?<!\d)(\d{1,3})\s*份(?:流程|规范)?文档",
    "测试数": r"(\d{1,4})\s*个(?:单元)?测试",
}
PLACEHOLDERS = ["TODO", "FIXME", "lorem ipsum", "待补充", "占位文本"]


class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.err, self.ids, self.imgs, self.anchors = [], [], [], [], []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.append(d["id"])
        if tag == "img":
            self.imgs.append(d.get("alt"))
        if d.get("href", "").startswith("#") and len(d["href"]) > 1:
            self.anchors.append(d["href"][1:])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.err.append(f"多余闭合 </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.err.append(f"<{self.stack.pop()}> 未闭合")
            self.stack.pop()
        else:
            self.err.append(f"孤立闭合 </{tag}>")


def local_target(page, url):
    u = urllib.parse.unquote(url.split("?")[0].split("#")[0])
    return (page.parent / u).resolve() if u else None


def case_mismatch(page, url):
    """逐级检查路径大小写。返回 (实际名, 期望名) 或 None"""
    u = urllib.parse.unquote(url.split("?")[0].split("#")[0])
    cur = page.parent
    for part in Path(u).parts:
        try:
            entries = os.listdir(cur)
        except OSError:
            return None
        if part in entries:
            cur = cur / part
            continue
        alt = [e for e in entries if e.lower() == part.lower()]
        return (alt[0], part) if alt else None
    return None


def make_opener(no_proxy=True):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    handlers = [urllib.request.HTTPSHandler(context=ctx)]
    if no_proxy:
        handlers.insert(0, urllib.request.ProxyHandler({}))  # 清空代理，才算别人能不能打开
    return urllib.request.build_opener(*handlers)


def probe(opener, url, timeout=8):
    t0 = time.time()
    try:
        with opener.open(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=timeout) as r:
            return {"ok": True, "status": r.status, "ms": int((time.time() - t0) * 1000)}
    except Exception as e:
        msg = f"HTTP {e.code}" if isinstance(e, urllib.error.HTTPError) else str(getattr(e, "reason", e))
        return {"ok": False, "error": msg[:80], "ms": int((time.time() - t0) * 1000)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--no-net", action="store_true", help="跳过外链联网测试")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--timeout", type=int, default=8)
    a = ap.parse_args()

    root = Path(a.root).resolve()
    pages = sorted(p for p in root.rglob("*.html"))
    if not pages:
        print(f"没找到 HTML：{root}", file=sys.stderr)
        return 1
    src = {p: p.read_text(encoding="utf-8", errors="ignore") for p in pages}

    blocking, warn = [], []
    R = {"root": str(root), "pages": len(pages), "round1": {}, "round2": {}, "round3": {}}

    # ── 轮 1 ────────────────────────────────────────────
    dead, case_bad, leak, total = [], [], [], 0
    externals = {}
    for p in pages:
        rel = str(p.relative_to(root))
        s = src[p]
        for m in ABS_LEAK.finditer(s):
            leak.append({"page": rel, "code": m.group(0)[:80]})
        for m in ATTR.finditer(s):
            u = m.group(1)
            if u.startswith(SKIP_SCHEME):
                if u.startswith("http"):
                    externals.setdefault(u, set()).add(rel)
                continue
            if not u:
                continue
            total += 1
            t = local_target(p, u)
            if t is None:
                continue
            if not t.exists():
                dead.append({"page": rel, "url": u})
            else:
                cm = case_mismatch(p, u)
                if cm:
                    case_bad.append({"page": rel, "url": u, "actual": cm[0]})

    R["round1"] = {"local_links": total, "dead": dead, "case": case_bad, "abs_leak": leak}
    blocking += [("死链", d) for d in dead] + [("大小写", c) for c in case_bad] + [("绝对路径", l) for l in leak]

    ext = []
    if not a.no_net:
        op = make_opener(no_proxy=True)
        for u in sorted(externals):
            r = probe(op, u, a.timeout)
            r["url"] = u
            r["pages"] = sorted(externals[u])
            ext.append(r)
            if not r["ok"]:
                warn.append(("外链不可达", u))
        R["round1"]["external"] = ext

    # ── 轮 2 ────────────────────────────────────────────
    problems = []
    for p in pages:
        rel = str(p.relative_to(root))
        s = src[p]
        c = TagChecker()
        c.feed(s)
        errs = list(c.err) + [f"<{t}> 未闭合" for t in c.stack]
        dup = sorted({i for i in c.ids if c.ids.count(i) > 1})
        miss = sorted({x for x in c.anchors if x not in c.ids})
        noalt = sum(1 for x in c.imgs if x is None)
        js_bad = []
        for js in SCRIPT.findall(s):
            if not js.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                f.write(js)
                tmp = f.name
            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            os.unlink(tmp)
            if r.returncode != 0:
                js_bad.append(r.stderr.strip().splitlines()[0][:100])
        norels = len([b for b in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', s) if "noopener" not in b])

        item = {"page": rel, "tags": errs[:4], "dup_ids": dup, "bad_anchors": miss,
                "img_no_alt": noalt, "js": js_bad, "blank_no_rel": norels,
                "title": "<title>" in s, "viewport": 'name="viewport"' in s}
        problems.append(item)
        if errs:
            blocking.append(("标签未配平", rel))
        if js_bad:
            blocking.append(("JS 语法", rel))
        for label, cond in [("重复 id", dup), ("锚点无目标", miss), ("缺 alt", noalt),
                            ("缺 title", not item["title"]), ("缺 viewport", not item["viewport"]),
                            ("缺 rel=noopener", norels)]:
            if cond:
                warn.append((label, rel))
    R["round2"] = problems

    # ── 轮 3 ────────────────────────────────────────────
    metrics, ph = {}, []
    for label, pat in METRIC_PROBES.items():
        hits = []
        for p in pages:
            for m in re.finditer(pat, src[p]):
                hits.append({"page": str(p.relative_to(root)), "value": m.group(1)})
        vals = sorted({h["value"] for h in hits})
        metrics[label] = {"values": vals, "hits": hits}
        if len(vals) > 1:
            warn.append((f"指标多值：{label}={vals}", "全站"))
    for w in PLACEHOLDERS:
        for p in pages:
            if w in src[p]:
                ph.append({"page": str(p.relative_to(root)), "word": w})
    if ph:
        warn.append((f"占位符残留 {len(ph)} 处（先看上下文，可能是代码）", "全站"))
    R["round3"] = {"metrics": metrics, "placeholders": ph}

    # ── 输出 ────────────────────────────────────────────
    if a.json:
        R["blocking"] = [{"kind": k, "detail": d if isinstance(d, str) else d} for k, d in blocking]
        R["warn"] = [{"kind": k, "detail": d} for k, d in warn]
        print(json.dumps(R, ensure_ascii=False, indent=1))
        return 1 if blocking else 0

    print(f"站点 {root}｜{len(pages)} 个页面\n")
    print("【第一轮·链接】")
    print(f"  本地相对链接 {total} 条｜死链 {len(dead)}｜大小写不一致 {len(case_bad)}｜绝对路径泄漏 {len(leak)}")
    for d in dead:
        print(f"    ✗ 死链 {d['page']} → {d['url']}")
    for c in case_bad:
        print(f"    ✗ 大小写 {c['page']}: {c['url']}（实际 {c['actual']}）")
    for l in leak:
        print(f"    ✗ 绝对路径 {l['page']}: {l['code']}")
    if ext:
        print(f"  外链 {len(ext)} 条（已绕开本机代理直连实测）")
        for r in ext:
            if r["ok"]:
                print(f"    {r['status']}  {r['ms']:>5}ms  {r['url']}")
            else:
                print(f"    ✗  {r['error']:<28} {r['url']}")

    print("\n【第二轮·结构】")
    for it in problems:
        bad = {k: v for k, v in it.items()
               if k in ("tags", "dup_ids", "bad_anchors", "img_no_alt", "js", "blank_no_rel") and v}
        if not it["title"]:
            bad["title"] = "缺失"
        if not it["viewport"]:
            bad["viewport"] = "缺失"
        print(f"  {'✗' if bad else '✓'} {it['page']}" + ("" if not bad else f"  {bad}"))

    print("\n【第三轮·内容】")
    for label, m in metrics.items():
        flag = "⚠️" if len(m["values"]) > 1 else "✓"
        print(f"  {flag} {label}: {m['values']}")
    if ph:
        print(f"  ⚠️ 占位符 {len(ph)} 处（先看上下文）")

    print(f"\n阻断 {len(blocking)} 项｜提醒 {len(warn)} 项")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
