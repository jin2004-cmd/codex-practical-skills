#!/usr/bin/env python
"""resume-jd-matcher 机检脚本：硬条件判定 + JD关键词覆盖率。

用法: python match_resume.py <JD.txt> <简历.txt>
输出 JSON: hard_requirements / keyword_coverage / duplicates
退出码: 0=成功, 2=错误
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

EDU = ["博士", "硕士", "本科", "大专", "统招"]
CERTS = ["英语四级", "英语六级", "CET-4", "CET-6", "PMP", "教师资格证",
         "CPA", "法考", "执业医师", "驾照", "C1", "C2"]
YEAR_RE = re.compile(r"(\d+)[-~到至]{0,2}(\d+)?\s*年")
LOC_WORDS = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京",
             "西安", "苏州", "郑州", "长沙", "重庆", "天津", "合肥", "青岛"]

SPLIT = re.compile(r"[，。；、！？\s（）()【】\[\]·,/|;:：!?\n]+")
STOP = {"的", "与", "和", "及", "或", "有", "熟悉", "了解", "掌握", "熟练", "优先",
        "具备", "能够", "负责", "相关", "工作", "以上", "岗位", "职责", "任职",
        "要求", "者", "等", "强", "良好", "优秀", "能力"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


VERB_PREFIX = re.compile(r"^(熟悉|了解|掌握|熟练|精通|具备|有|会用|使用|负责|优先)+")
TAIL_SUFFIX = re.compile(r"(者优先|经验|能力|意识|精神|经历|思维)+$")


def extract_jd_terms(jd):
    """拆词：标点切分→再按与/和/及切→剥离动词前缀与后缀。"""
    raw = []
    for w in SPLIT.split(jd):
        w = w.strip()
        if not w:
            continue
        for part in re.split(r"[与及和]", w):
            part = VERB_PREFIX.sub("", part.strip())
            part = TAIL_SUFFIX.sub("", part.strip())
            if part:
                raw.append(part)
    NOISE = {"任职要求", "岗位职责", "以上学历", "工作经验", "相关经验", "工作内容", "优先考虑"}
    return [w for w in raw if 1 < len(w) <= 12 and w not in STOP and w not in NOISE
            and "学历" not in w and w not in CERTS and not re.fullmatch(r"[\d.%~-]+", w)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jd_file")
    ap.add_argument("resume_file")
    args = ap.parse_args()
    for p in (args.jd_file, args.resume_file):
        if not os.path.isfile(p):
            print(json.dumps({"error": "文件不存在: %s" % p}, ensure_ascii=False))
            sys.exit(2)

    jd, resume = read(args.jd_file), read(args.resume_file)
    res_low = resume.lower()

    # --- 硬条件 ---
    hard = []
    edu_jd = [e for e in EDU if e in jd]
    if edu_jd:
        top = edu_jd[0]  # JD 通常写最低要求，取最高档出现在JD中的
        order = ["大专", "本科", "硕士", "博士"]
        need = max(edu_jd, key=lambda e: order.index(e) if e in order else -1)
        hard.append({"type": "学历", "require": need,
                     "status": "达标" if any(EDU.index(e) >= EDU.index(need)
                                            for e in EDU if e in resume) else "未提及/缺失"})
    years = YEAR_RE.findall(jd)
    if years:
        n = int(years[0][0])
        m = re.findall(r"(\d{4})[.\-/年]\s*(\d{1,2})?", resume)
        span = 0
        if len(m) >= 2:
            spans = []
            for a, b in zip(m, m[1:]):
                dy = int(b[0]) - int(a[0])
                spans.append(max(0, dy))
            span = max(spans)
        if span >= n:
            ys = "达标(简历日期可推算约%d年)" % span
        elif span > 0:
            ys = "差距(简历日期推算约%d年，不足%d年，如实标注不建议凑)" % (span, n)
        elif len(m) == 1:
            ys = "未提及(简历仅含单个日期，无法推算年限，请人工核对)"
        else:
            ys = "未提及(简历无可推算的工作日期)"
        hard.append({"type": "经验年限", "require": "%d年" % n, "status": ys})
    for c in CERTS:
        if c in jd:
            hard.append({"type": "证书", "require": c,
                         "status": "达标" if c.lower() in res_low else "未提及/缺失"})

    # --- 关键词覆盖 ---
    terms = list(dict.fromkeys(extract_jd_terms(jd)))
    hit, miss, semantic_hint = [], [], []
    for t in terms:
        if t in resume:
            hit.append(t)
        elif any(ch in resume for ch in t if len(t) > 3) and len(t) > 3:
            # 部分命中：超过一半字符出现，提示语义改写
            common = sum(1 for ch in t if ch in resume)
            (semantic_hint if common >= max(2, len(t) // 2) else miss).append(t)
        else:
            miss.append(t)
    coverage = round(len(hit) / len(terms) * 100, 1) if terms else 0

    # --- 重复度预警 ---
    res_lines = [ln.strip() for ln in resume.splitlines() if len(ln.strip()) > 12]
    dup = [ln for ln, c in Counter(res_lines).items() if c > 1]

    print(json.dumps({
        "hard_requirements": hard,
        "keyword_coverage": {"total_terms": len(terms), "hit": hit, "missing": miss,
                             "partial_semantic_check": semantic_hint,
                             "coverage_pct": coverage},
        "duplicate_lines": dup,
        "note": "partial_semantic_check 为疑似同义改写，由AI层人工判定；不建议编造未做过的经历",
    }, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
