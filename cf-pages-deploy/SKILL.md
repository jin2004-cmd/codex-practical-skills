---
name: cf-pages-deploy
description: 把 GitHub 上的纯静态前端仓库（HTML/CSS/JS、无构建）一键部署到 Cloudflare Pages，得到 `<project>.<account>.workers.dev` 地址并随 push 自动重新部署。⚠️ 2026-10-26 实测更正：**workers.dev 在境内多数网络被 DNS 污染、直连不通**，只能当自用/翻墙备份，**不要拿它当"国内免翻墙地址"给外部的人**——要给面试官/客户看的站请用 `*.github.io`。Gitee Pages 已永久下线，不要再试。
version: 1.1.0
---

# CF Pages 一键部署国内镜像

> ## ⚠️ 勘误（2026-10-26，v1.0.0 的核心结论被实测推翻）
>
> 本文件原写「生成国内免翻墙可访问的 `*.workers.dev` 地址」「这就是国内免翻墙地址」
> 「workers.dev 电信联通秒开」——**这三句是错的**。
>
> 2026-10-26 在境内直连（不挂任何代理）实测三个已部署子域：
>
> | 子域 | 境内直连 | DNS 解析到 |
> |---|---|---|
> | `talkcal.jinjiaxin2004.workers.dev` | ❌ 超时 | 173.255.213.90 |
> | `daypilot.jinjiaxin2004.workers.dev` | ❌ 超时 | 31.13.96.195（Meta 的 IP 段） |
> | `ai-video-portfolio.jinjiaxin2004.workers.dev` | ❌ 超时 | 67.228.235.91 |
>
> 同一时刻 `*.github.io` 直连 **184–698 ms 全 200**。
>
> **代价**：作品集首页三个「在线版（免翻墙）」按钮 + 视频页 12 条成片的 `<video src>`
> 全挂在这些 workers.dev 上 → 面试官点开一个都播不了，页面还写着"免翻墙"。
>
> **修正后的用法**：`cf-pages-deploy` 仍然值得用（自动重新部署、无广告、免费），
> 但**产物只能给"翻墙的人"或"自己"看**。要给外部人看的静态站，托管首选 GitHub Pages。
> 判定方法见 `static-site-deploy-verify` 第一部分的「可达性判定表」。


## 何时用
- 用户说"部署到国内""国内镜像""免翻墙打开""映射一份到国内网页"
- 仓库是纯静态（index.html 在根目录，无 npm build）
- 本地 `git push` 被 GFW 443 卡住，必须走 GitHub MCP

## 死路清单（别再试，浪费时间）
- ❌ **Gitee Pages**：2023 年起因监管永久下线，新账号菜单里根本没有入口（官方 issue I9RGKI / IA6DQ6 / I6YDKR 确认）
- ❌ **gh-proxy.com / ghfast.top / ghproxy.net**：只代理 raw 文件，不代理 `*.github.io` 整站，全部 403/404
- ❌ **本地 git push origin**：GFW 443 必挂，改用 MCP `push_files`

## 标准流程（10 分钟）

### 1. 确认仓库有 index.html
用 MCP `get_file_contents` 看根目录，必须有 `index.html`。Python 技能包、纯 README profile 仓库跳过。

### 2. 浏览器登录 Cloudflare
- 打开 https://dash.cloudflare.com
- 用 GitHub OAuth 登录（**注意：Chrome 可能登错账号，先去 github.com 确认是目标账号，再回 CF**）
- 路径：左侧 Compute → Workers & Pages → Create application → Connect GitHub

### 3. 授权 GitHub App
- 弹窗里确认账号名是用户本人（不是另一个 GitHub 号）
- 选 "All repositories" 或 "Only select repositories" → Install & Authorize

### 4. 选仓库
- 下拉选目标 repo → Next
- Project name 默认（会变成 `<name>.<account>.workers.dev`）
- Build command **留空**，Root directory `/`
- 点 Deploy

### 5. 拿地址
- 构建 25s 左右完成（绿勾）
- 点右上角 Visit，URL 形如 `https://<project>.<account>.workers.dev/`
- ~~这就是国内免翻墙地址~~ → **更正（2026-10-26）：这是一个"有墙时才打得开"的地址**。
  自用、翻墙看、当备份都行；**发给外部的人就是死链**（实测三个子域境内直连全超时）。

### 6. 自动同步
- Cloudflare 已绑定 GitHub，以后每次 `git push origin main` 自动重新部署，**零操作**

## 常见坑
- **Chrome 登错 GitHub 账号**：OAuth 弹窗显示的账号不是用户的 → 去 github.com 头像 → Sign out from all accounts → 重新登录目标账号 → 回 CF 重来
- **新 Workers 流程要 Build command**：纯静态项目直接留空即可，CF 自动识别
- ~~**国内访问速度**：workers.dev 电信联通秒开，移动偶尔慢~~ → **更正**：那是挂了代理时的速度。
  境内直连是被 **DNS 污染**（解析到 `31.13.x` 这类 Meta 段），不是"慢"，是**根本连不上**。
  要确认，`nslookup <子域>`：正常应该是 Cloudflare 段，见到 `31.13.x` / `2a03:2880:` 就是被劫持。
  另外：本机如果挂着代理，`curl` 测出来的是"代理能开"，**必须 `--noproxy '*'` 才算数**。
- **"Missing git connection" 报错**：GitHub App 已选 All repositories 仍报此错，是 CF 前端缓存。**刷新当前创建页（F5）后重走一遍选仓库流程即可**，不要去 GitHub 改授权，权限本来就有。
- **点仓库旁箭头跳转 github.com 是对的**：用来确认仓库存在和 index.html 位置，不是让你在那授权。

## 已部署清单（jin2004-cmd 账号，2026-10-17）
> ⚠️ 下表全部是 `workers.dev`，**境内直连不通**。这些地址只适合自己翻墙访问或做备份；
> 对外分享请用同名仓库的 `https://jin2004-cmd.github.io/<repo>/`（实测可用）。
| 仓库 | 国内镜像地址 |
|---|---|
| talkcal | https://talkcal.jinjiaxin2004.workers.dev/ |
| ai-video-portfolio | https://ai-video-portfolio.jinjiaxin2004.workers.dev/ |
| ad-compliance-checker | https://ad-compliance-checker.jinjiaxin2004.workers.dev/ |
| ecom-script-agent | https://ecom-script-agent.jinjiaxin2004.workers.dev/ |
| daypilot | https://daypilot.jinjiaxin2004.workers.dev/ |

跳过的仓库：jin-memory-sync（私人记忆）、codex-practical-skills（Python 技能包非网站）、jin2004-cmd（profile README）、awesome-claude-skills / awesome-codex-skills（fork）。

## 相关工具
- GitHub MCP `push_files`：本地 git 不通时用它推代码
- GitHub MCP `get_file_contents`：确认仓库结构
- 浏览器：`computer_use_tool` plane="cu" 驱动 Chrome
