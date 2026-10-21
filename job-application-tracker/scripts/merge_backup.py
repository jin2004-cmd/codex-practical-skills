#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
merge_backup.py — 用「用户导出的备份」重建底表。

使用场景：工具页面支持导出 JSON 备份。用户在外面改了数据（新增 / 改状态 / 删除），
把备份发回来要求合并。此时**备份是最新真相**，底表是旧快照。

处理原则：
1. 备份 = 真相，**包括用户做的删除**（底表有、备份没有 → 他删了，跟着删）
2. 但有些字段是我在别的环节挖出来的资产（如从原始表回填的投递链接），
   备份里可能丢失 → 按名字回填，**只填空，不覆盖已有**
3. 合并后必须做撞名检测

用法：python merge_backup.py <备份.json> [底表.json]
     默认底表 = _merged_seed.json
"""
import io
import json
import os
import re
import sys

DEFAULT_SEED = "_merged_seed.json"


def norm(s):
    """保守归一化：只去括号内容、空白、公司后缀。

    🔴 绝对不要去掉「集团 / 科技 / 技术 / 网络」这类词：
       TCL科技 和 TCL 是两家不同的公司主体，去掉就撞了。
       锐捷网络 / 锐捷 同理。
    """
    s = str(s or "").strip()
    s = re.sub(r"[（(].*?[)）]", "", s)      # 去掉括号及内容
    s = s.replace(" ", "").replace("\u3000", "")
    s = re.sub(r"(股份有限公司|有限公司|股份公司)$", "", s)
    return s


def load(path):
    if not os.path.isfile(path):
        print("文件不存在: %s" % path)
        sys.exit(2)
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main(backup_path, seed_path=DEFAULT_SEED):
    bk = load(backup_path)
    old = load(seed_path)

    cs = bk.get("companies") or []
    old_recs = old["companies"] if isinstance(old, dict) and "companies" in old else old

    print("备份 : %s" % os.path.basename(backup_path))
    print("  exportedAt : %s" % bk.get("exportedAt"))
    print("  snapshot   : %s" % bk.get("snapshot"))
    print("  companies  : %d" % len(cs))
    print("旧底表 companies: %d" % len(old_recs))

    # --- 1. 备份内部同名去重（保留首条）---
    seen, dups = {}, []
    for c in cs:
        raw = str(c.get("name") or "").strip()
        if raw in seen:
            dups.append(raw)
        else:
            seen[raw] = c
    if dups:
        print("  ⚠ 备份内部同名重复(已合并): %s" % dups)
    cs = list(seen.values())

    # --- 2. 建旧底表的「资产字段」索引（这里以 url 为例，按需扩展）---
    urlidx = {}
    for x in old_recs:
        u = str(x.get("url") or x.get("u") or "").strip()
        if u:
            urlidx.setdefault(norm(x.get("n")), u)

    # --- 3. 重建 ---
    out, filled = [], 0
    for i, c in enumerate(cs):
        rec = {
            "id": c.get("id") or ("u_%d" % i),
            "n": str(c.get("name") or ""),
            "c": str(c.get("cat") or ""),
            "s": str(c.get("status") or "已投"),
            "j": max(0, int(c.get("jobs") or 0)),
            "d": str(c.get("ddl") or ""),
            "l": str(c.get("loc") or ""),
            "k": str(c.get("code") or ""),
            "o": str(c.get("note") or ""),
            "url": str(c.get("url") or ""),
            "a": 1 if c.get("archived") else 0,
            "h": 1 if c.get("hist") else 0,
        }
        if not rec["url"]:
            k = norm(rec["n"])
            if k in urlidx:
                rec["url"] = urlidx[k]
                filled += 1
        out.append(rec)

    # --- 4. 撞名检测 ---
    names = {}
    for r in out:
        names.setdefault(norm(r["n"]), []).append(r["n"])
    clash = {k: v for k, v in names.items() if len(v) > 1}
    if clash:
        print("\n⚠ 归一化后撞名（需要人工确认是否同一家）:")
        for k, v in clash.items():
            print("   %s ← %s" % (k, " / ".join(v)))
    else:
        print("\n✅ 无撞名")

    # --- 5. 疑似重复检测（只报告，绝不自动合并）---
    # 第 4 条匹配规则「双向包含」风险最高：携程旅行 ⊃ 携程 是真的，
    # 但 TCL科技 ⊃ TCL 是两家不同的公司主体。
    # 所以这里只列出来给人看，合并动作必须人工下命令。
    keys = [norm(r["n"]) for r in out]
    suspect = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            if not a or not b or a == b:
                continue
            if a in b or b in a:
                suspect.append((out[i]["n"], out[j]["n"]))
    if suspect:
        print("\n⚠ 疑似重复（包含关系，人工确认后再决定是否合并）:")
        for a, b in suspect:
            print("   %s  ~  %s" % (a, b))
    else:
        print("\n✅ 无疑似重复")

    print("\n结果: %d 家，其中回填资产字段 %d 家" % (len(out), filled))

    with io.open(seed_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("已写回 %s" % seed_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SEED)
