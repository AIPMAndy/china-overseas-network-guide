# 官方来源、社区资料与核验口径

**来源核查：2026-10-12。**项目选择“官方设计说明 + 有限社区反例 + 明确未实测”，不刊登个人节点、商家链接、邀请码或付费排名。网页的搜索可达性及出版内容可能随时间变化。

## 法规、官方说明（A级）

| 主题 | 原始来源 | 支持什么 | 不支持什么 |
|---|---|---|---|
| 国际联网原则 | [国际联网管理暂行规定](https://hbca.miit.gov.cn/xxgk/zcwj/flfg/art/2020/art_b118b9e4e97d4a8e9e6af358c78ac4dc.html) | 有关中国国际联网管理的法规来源 | 个体用途的无条件合法性保证 |
| 跨境经营 | [工信部 2017 通知](https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2017/art_a940645e940946e1a62cd6c90a4e994e.html) | 关于未批准跨境经营和跨境专线使用的规则 | 所有个人/企业行为的单一定性 |
| Outline | [官方开始使用](https://getoutline.org/get-started/) / [配置文档](https://developer.getoutline.org/zh-CN/vpn/management/config/) | Manager、Client、授权密钥、代理实现 | 国内当日连接成功率 |
| Amnezia 自建 | [官方教程](https://docs.amnezia.org/documentation/instructions/install-vpn-on-server/) / [FAQ](https://docs.amnezia.org/faq/) | 官方协议、客户端、安装及“中国未专测”限制 | 适合所有中国网络 |
| AmneziaWG | [官方协议](https://docs.amnezia.org/documentation/amnezia-wg/) | 不同版本设计与混淆思路 | “绝不被检测”的保证 |
| Hysteria 2 | [官网](https://hysteria.network/) / [服务端安装](https://hysteria.network/docs/getting-started/Server/) | QUIC/UDP 架构和官方部署条件 | 所有运营商必然更快 |
| Xray/REALITY | [XTLS/Xray-core](https://github.com/XTLS/Xray-core) | 官方项目、部署示例和协议生态 | 未核验第三方一键脚本安全 |
| v2rayN | [2dust/v2rayN](https://github.com/2dust/v2rayN) | Windows/Linux/macOS 图形工具及版本 | 自动附赠网络服务 |
| Mihomo | [MetaCubeX/mihomo Releases](https://github.com/MetaCubeX/mihomo/releases) | 核心维护与发布包 | 任何非官方镜像/“破解”可信 |
| Clash Verge Rev | [项目仓库](https://github.com/clash-verge-rev/clash-verge-rev) | 桌面图形客户端 | 自带授权节点 |
| sing-box | [项目文档](https://sing-box.sagernet.org/) | 核心/客户端生态，版本变动 | 未经实测的区域成功率 |
| Tailscale | [Exit nodes](https://tailscale.com/docs/features/exit-nodes) | Exit Node 概念、权限和操作路径 | 受限网络永远可达 |
| Tor | [官方网桥教程](https://support.torproject.org/tor-browser/circumvention/using-bridges/) | Tor 浏览器网桥的配置流程 | 高速、所有 App 共用 |
| Cloudflare WARP | [官方模式](https://developers.cloudflare.com/warp-client/warp-modes/) | 路由保护和非匿名/非伪装国家的局限 | 任选国家出口 |
| Apple eSIM | [中国大陆 eSIM 适用机型](https://support.apple.com/zh-cn/123879) / [数据漫游](https://support.apple.com/zh-cn/109037) | 具体机型、运营商设置与漫游步骤 | 全部境外旅行 eSIM 的兼容承诺 |
| GitHub Pages | [官方配置来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | 静态阅读页面发布 | 仓库内容审计 |

## 社区观测（C 级）：只看具体失败模式，不直接排名

详见 [RESEARCH_LOG.md](RESEARCH_LOG.md)：包括 2026-10-08 r/chinatravel、2026-10-10 r/VPNforFreedom 等近期讨论，以及 X 检索限制造成的证据缺口。社区帖子时间与事实发生时间须区分；不得凭一篇帖子的感受声称“稳定率 X%”。

## 来源四级与约束

- **A：官方原始资料**，可支持产品功能与规则陈述。
- **B：充分描述测量方法的复现报告**，可支持给定条件的测试结果。
- **C：第一手社区经历**，用于发掘风险和对抗案例。
- **D：营销、返佣、匿名转述**，不用于排名或结论。

凡是带“原生住宅 IP、专线、纯净、永久、绝对安全”的营销说法，必须有可复核的合同、技术路径或实测数据才可能成为主张；任何 IP 归属地标签都不能证明平台会员资格、支付主体或个人居住地。


## v3.0 新增的官方核验资料（2026-10-12）

| 主题 | 官方材料 | 在新增策略中的用法与边界 |
|---|---|---|
| Tailscale 出口及权限 | [Exit nodes](https://tailscale.com/docs/features/exit-nodes) | 说明出口节点需设备配置和管理员许可；不证明中国任意网络可达 |
| Tailscale 路由切换 | [Route selection](https://tailscale.com/docs/features/route-selection) / [HA](https://tailscale.com/kb/1115/subnet-failover/) | 说明特定连接器的备用机制；不泛化为任意 VPN 自动切换 |
| Cloudflare IP/DNS 分流 | [Split Tunnels](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/route-traffic/split-tunnels/) | 明确分流 IP 和 DNS 可能采用不同策略；不证明具体代理能规避网络限制 |
| Apple 管理式 VPN | [VPN overview](https://support.apple.com/guide/deployment/vpn-overview-depae3d361d0/1/web/1.0) | VPN On Demand 与 Per-App VPN 的功能和管理前提；普通 App 不一定支持 |
| Docker daemon 与 Desktop | [Docker daemon proxy](https://docs.docker.com/engine/daemon/proxy/) | 区分 daemon、Desktop 和容器网络设置；不证明具体国内镜像站可靠 |
| GitHub 安全与恢复 | [Security overview](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure) / [2FA recovery](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials) | 密码、MFA、Token、账号恢复；不保证遭入侵后全部可恢复 |

新增章节中的故障剧本均标明为**可复现实验场景**，尚非作者本人在中国大陆完成的实测案例。所有性能阈值、成本与切换间隔都是教学用的**可调整假设**。
