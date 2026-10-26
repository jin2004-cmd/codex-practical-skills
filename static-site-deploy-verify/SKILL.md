---
name: static-site-deploy-verify
description: 静态站（GitHub Pages / Cloudflare Pages / 任意 CDN）发布前后的全流程校验。推之前跑三轮体检（链接 / 结构 / 内容），推之后抓「缓存名 bump 了但文件内容还是旧的」这类版本撕裂，并判定「打不开到底是墙、DNS 污染、公司网络还是站真挂了」。适用于「帮我确认线上是不是最新的」「我改了但线上还是老样子」「作品集要发给面试官了，先体检一遍」「这个链接国内能打开吗」。
version: 1.1.0
---

# 静态站发布前后校验

## 何时用
- 用户反馈「我改了但线上没变」「还是上个版本」
- 刚刚推送完静态站，用户要求确认线上是最新的
- Service Worker / PWA 项目，怀疑缓存没失效
- **要把站点发给外部的人（面试官、客户、HR）之前** → 先跑三轮体检
- 问「国内能不能打开」「要不要翻墙」 → 先看下面的可达性判定

---

# 第一部分：推之前 —— 三轮体检

顺序不能换。**链接轮不通过，后面两轮没有意义**（面试官点开就是 404，内容写得再好也没用）。

跑 `scripts/preflight_audit.py --root <站点目录>`，或按下面的清单手工过。

## 第一轮 · 链接与可达性

| 检查项 | 为什么必须查 |
|---|---|
| 本地相对链接是否都存在 | 死链 |
| **大小写是否一致** | Pages 跑在 Linux 上**区分大小写**，Windows 本地不区分。`Shots/A.jpg` 在本地能开、线上 404 —— 这类 bug 只在线上炸 |
| 是否有 `file:///` 或 `D:\` 绝对路径泄漏 | 从本地文件直接改的 HTML 常带出来，线上必挂 |
| **外链是否真的能直连** | 见下 |

### 外链必须「绕开本机代理」测

本机常挂着代理，走代理能打开**不代表**别人能打开。这个假阳性害过一次：
`*.workers.dev` 在代理下 502、在直连下超时，**只有直连的结果才算数**。

```python
import urllib.request
# 关键：ProxyHandler({}) 清空代理
direct = urllib.request.build_opener(urllib.request.ProxyHandler({}))
```
先 `env | grep -i proxy` 确认环境里有没有 `HTTP_PROXY`。有的话，不绕开测出来全是假的。

### 可达性判定表（国内实测，2026-10 复核）

| 域名 | 境内直连 | 结论 |
|---|---|---|
| `*.github.io` | ✅ 184–698 ms，全 200 | **静态站首选**，不用翻墙 |
| `github.com` | ⚠️ 能开但慢且不稳（0.7–1.4 s，偶发超时） | 仓库页可以给，但别拿它当展示页 |
| `*.workers.dev` | ❌ **系统性不可用** | 见下 |
| `gh-proxy.com` | ⚠️ 只代理 raw / release | 拿它代 `*.github.io` 会 404 |

**`*.workers.dev` 是被 DNS 污染，不是偶尔抽风。** 实测三个子域解析到：

```
talkcal.jinjiaxin2004.workers.dev          → 173.255.213.90
daypilot.jinjiaxin2004.workers.dev         →  31.13.96.195   ← Meta/Facebook 的段
ai-video-portfolio.jinjiaxin2004.workers.dev →  67.228.235.91
```

`31.13.x` / `2a03:2880:` 是 Meta 的 IP 段 —— 解析到这儿就等于被劫持了。
识别方法：`nslookup <domain>`，看是不是 `185.199.x`（真正的 GitHub Pages）。

> 翻车实录：作品集首页三个按钮写着「在线版（免翻墙）」指向 `workers.dev`，
> 而视频页 **12 条成片的 `<video src>` 全在 workers.dev 上** —— 面试官点开一个都播不了，
> 页面却写着"免翻墙"。**凡是要给外部人看的静态站，别用 workers.dev。**

**结论：站点托管优先 `github.io`；`workers.dev` 只能当"自己人翻墙看"的备份，不能写进给面试官的页面。**

## 第二轮 · 结构与运行时

| 检查项 | 常见炸法 |
|---|---|
| 标签配平 | 少一个 `</div>` → 后面整块布局塌 |
| 重复 `id` | `getElementById` 只认第一个，跳转/筛选全乱 |
| 锚点 `#xxx` 有没有目标 | 点了没反应 |
| `data-goto` 之类的自定义跳转目标存不存在 | 同上，而且是"看着有交互其实没生效" |
| `<img>` 有没有 `alt` | 图挂了只剩破图框 |
| `<title>` + viewport | 手机端按 980px 排版，字小到看不清 |
| **内联脚本语法** | 用 `node --check` 逐个过 |
| `target="_blank"` 有没有 `rel="noopener"` | 被打开页能通过 `window.opener` 反向操作本站 |

`node --check` 的坑：**`<script type="application/ld+json">` 不是 JS**，
里面是 JSON-LD，直接丢给 `node --check` 会报 `SyntaxError: Unexpected token ':'`。
必须按 `type` 跳过，否则每次都误报。

## 第三轮 · 内容与数字一致性

1. **同一个指标全站只能有一个值。** 用正则把所有出现位置列出来，`len(set(值)) > 1` 就是问题。
2. **同一个数字可能有两个含义，不要合并。** 项目里「27」既是 27 条自动替换规则、也是 27 个测试函数——
   两个都是真的。（后来测试涨到 35，替换规则仍是 27。）
3. **改数字要回头改所有引用处**，包括 meta description、镜像站、README、CHANGELOG。
4. **镜像站（如果有）要和源页同步**：把前缀差异归一化后逐行 diff，差异应该只有"应删的那几块"。
5. 扫一遍 `TODO` / `lorem` / `待补` / `undefined` / `NaN` / `xxx` —— 但**先看上下文**：
   本次 11 处命中全部是 JS 关键字和 base64 poster 里的字符，零真问题。别把代码当占位符。

---

# 第二部分：发布

## 铁律：判断线上版本用 GitHub API 查文件，不信本地 `git log`

MCP `push_files` 之类的推送**不产生本地 commit**，`git log` 会停在旧版本，误判成"线上版本不明"。

```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=main"
```

**CHANGELOG 说改过 ≠ 真的改过。** 翻车实录：CHANGELOG v1.0.5 明确写"把 27 改成 35"，
但把线上 `index.html` 拉下来一看还是 27 —— 记录写了、文件没动。
**任何"已经改好了"的说法，都要拉文件实测一次。**

## 公开站 ≠ 打包件：允许有意的差异，但必须机械保证

给面试官的**打包文件夹**里可以放实习公司的内部 SOP；
**公开站点**不能放同样的东西。同一份 `index.html` 两个去向时：

- 本地保持原样（PDF 链接照旧）
- 推送副本用 `.replace()` 改那几处，并且 **`assert count == 1`**
- 推完把本地 vs 远端 diff 出来，**差异行数必须等于预期**（3 处替换 = 6 行）

这样"故意不同"就变成了可验证的断言，而不是靠人记得。

---

# 第三部分：推之后 —— 部署校验

## 核心洞察：版本撕裂
只 bump 缓存名而不推齐文件 = **缓存名是新的、内容还是旧的**，用户端会长期命中旧缓存，表现为"我改了没效果"。

修复必须**两步一起做**：
1. 把所有不一致的文件推齐
2. 把 `sw.js` 里的 `const CACHE` 再 bump 一次（不 bump 的话用户端仍命中旧缓存）

## 标准流程

### 1. 先跑一遍五类检查
| # | 检查项 | 做什么 |
|---|---|---|
| 1 | **漏推** | 本地有的文件远端没有 |
| 2 | **内容不一致** | 同名文件本地/远端 size 或 sha 不同（这是版本撕裂的根因） |
| 3 | **SW 缓存清单** | `sw.js` 里列出的文件是否与实际部署的文件对齐 |
| 4 | **HTML 引用** | `index.html` 引用的 css/js/img 是否全部存在（防 404） |
| 5 | **PWA 三件套** | manifest.json / sw.js / icon 是否齐全且互相引用一致 |

### 2. 具体做法
```bash
# 拿远端文件清单 + size/sha
curl -s "https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1"

# 逐个比对本地 size
# 注意：>1MB 的文件 contents API 不返回 base64（encoding: none）
#       要改用 GET /repos/<owner>/<repo>/git/blobs/<sha>
```

blob sha 可以直接在本地算，不用下载：`sha1("blob " + len + "\0" + content)`。
比对 sha 比比对 mtime 可靠——mtime 会因为拷贝、解压、同步全变。

### 3. Pages 构建状态与 CDN 滞后
```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/pages/builds/latest"
```
`status: built` **不等于** CDN 已经换新。刚 built 完那几十秒里，新文件仍可能 404。
加 `?v=<timestamp>` 复测，别一看到 404 就判"推失败了"。

### 4. 修复后必须强刷验证
改完让用户 **Ctrl+Shift+R**（不是 F5，F5 可能仍走内存缓存）再看。
⚠️ 这一步**必须由人在浏览器里做**，AI 无法代验——本机网络能否访问目标域名跟线上是否可用是两回事。

### 5. 判断"到底是网络问题还是站点挂了"
```bash
nslookup <domain>
```
- 解析到 **185.199.x** → GitHub Pages 真实 IP，正常
- 解析到 **31.13.x / 2a03:2880:** → 这是 **Meta/Facebook 的 IP 段**，说明 DNS 被劫持/污染，**不代表站点故障**
- 全部超时 → 换手机流量或非公司网再验一次再说

## Example

> 用户：「我更新了 TalkCal 的 css，但线上还是老样子。」

1. API 查远端 `css/style.css` 的 size，对比本地 → 发现本地 20987 B / 远端 18035 B，**内容不一致**
2. 同时查 `js/calendar.js` → 同样不一致
3. 检查 `sw.js` 的 `const CACHE` → 已经是 `talkcal-v2.6.1`（说明之前只 bump 了缓存名没推内容）
4. 修复：推齐两个文件 **+** CACHE bump 到 `talkcal-v2.6.2`
5. 等 CDN 自动重新部署，跑一遍第 1 步的五类检查确认全部对齐
6. 让用户 Ctrl+Shift+R 验收

## Example 2（发布前体检救回来的）

> 用户：「作品集要发给面试官了，确认一下不翻墙能看吗。」

1. 第一轮外链：本机挂着代理，走代理测 `*.workers.dev` 是 502、直连是超时 → **绕开代理重测**
2. `nslookup` 三个 workers.dev 子域 → 解析到 `31.13.96.195`（Meta 段），确认被污染
3. 顺藤摸瓜：视频页 **12 条 `<video src>` 全在 workers.dev 上**，首页 3 个按钮也是
4. 换成 `jin2004-cmd.github.io/ai-video-portfolio/assets/...`，直连实测 184–698 ms 全 200
5. 第二轮：`node --check` 报错 → 打开看是 JSON-LD，给检查器加 `type` 过滤，真问题 0
6. 第三轮：英文名两处不一致（旧名 vs 现行名）→ 统一；`82%` 是表单示例不是业绩声明 → 不改
7. 推 → Pages `built` → 加 `?v=` 复测 → 线上 `workers.dev` 计数归零

## 坑位清单
- `curl` 在公司网络下可能需要 `--noproxy '*'`，否则拿到假的连接失败
- **本机能打开 ≠ 别人能打开**：本机代理会把 `workers.dev` 测成"有时能开"
- `*.workers.dev` / `*.supabase.co` 常被公司 DNS 或墙拦；`*.github.io` 反而直连可用
- 大小写只在线上炸，本地永远测不出来
- 改 `sw.js` 缓存名但忘记推文件内容 = 白改；推了内容但忘记 bump = 用户端还是旧的
- Pages `built` 之后 CDN 仍可能滞后几十秒
- JSON-LD 不是 JS，别丢给 `node --check`
- 本地 git 历史与线上 API commit 分叉（如 `ahead 1`）时，先确认内容一致再决定是否 `git reset --hard origin/main`
