# 26｜开发者实战：Mac、Windows、终端、IDE 与 Docker

**目标：**彻底弄清“浏览器能用而 Git/Node/Python/Codex/IDE/Docker 不能用”的原因。以下命令主要用于诊断**已授权的企业代理或本机受信任代理**；端口为示例，必须替换为你自己在客户端确认的端口，不提供第三方连接凭据。

## 一、先画清五层

`接入网络（Wi-Fi/蜂窝） → 操作系统路由 → DNS → 应用的代理配置 → 目标 HTTPS 服务`

- 系统代理：通常影响遵循 OS 代理设置的应用；CLI/守护进程可能不遵循。
- `HTTP_PROXY`/`HTTPS_PROXY`：很多命令行工具读取，但不是所有工具都读取；变量值可能被子进程继承。
- TUN/VPN：改变部分或全部 IP 路由，不等同于“每个 DNS 查询已经得到正确处理”。
- Docker：Docker Desktop 与 Linux daemon 的配置地点可能不同。**官方明确：Docker Desktop 不读取 daemon.json 中的 daemon 代理配置。**[Docker 官方](https://docs.docker.com/engine/daemon/proxy/)
- Git/IDE：IDE 中的 Git/终端也可能有独立设置和环境变量。

## 二、Mac 安全诊断（不打印订阅信息）

打开终端，先运行：

```bash
# 网络服务名称可因电脑而异；先列出再选具体服务
networksetup -listallnetworkservices
# 查看当前系统首选网络下的公开路由（仅诊断）
route -n get default | head -20
# 仅列出是否存在代理环境变量，不显示其值或密钥
( env | cut -d= -f1 | grep -Ei '^(http|https|all|no)_proxy$' ) || true
# 查看 DNS 汇总可能很长，分享日志前人工脱敏
scutil --dns | head -60
```

然后按顺序：①浏览器加载公开文档；②在终端测试公开目标；③检查 IDE 内置终端；④若必要，检查 Docker。

**临时验证**（以下为本机示例监听地址；将 `7890` 改为你的实际合法配置监听端口）：

```bash
# 直接检查公开网页，10 秒无响应就停止
curl -I -L --max-time 10 https://example.com
# 仅诊断 HTTP 代理是否可用，不会永久修改系统设置
curl -I -L --max-time 10 --proxy http://127.0.0.1:7890 https://example.com
# 如果使用 Git，测试公共仓库的 HTTPS 元数据
HTTPS_PROXY=http://127.0.0.1:7890 \
 git ls-remote https://github.com/git/git.git HEAD
```

**注意**：连接失败时，不要用 `curl -k`、`GIT_SSL_NO_VERIFY=1` 或取消 TLS 校验“修复”；这可能隐藏证书中间人、代理错误和服务器身份问题。示例 `example.com` 测试不证明目标服务在中国大陆可访问。

## 三、Windows 最小诊断

PowerShell（不要粘贴含密钥的真实输出到公开提问）：

```powershell
# DNS 状态与 IP 配置
Get-DnsClientServerAddress | Select-Object -First 10
# 只显示变量是否设置；不显示密码和地址
Test-Path Env:HTTPS_PROXY
# 测试 HTTPS DNS/HTTP 请求；只用公开目标
Test-NetConnection example.com -Port 443
curl.exe -I --max-time 10 https://example.com
```

检查 Windows「设置 → 网络和 Internet → 代理」中的系统代理是否与本机客户端一致。若有企业 VPN/MDM，优先通过 IT 排查而非自行覆盖策略。

## 四、CLI 的正确处理顺序

1. **只浏览器失败：**先查浏览器扩展/代理/PAC；不用立刻动全机设置。
2. **浏览器正常而终端失败：**先检查终端变量和工具自己的代理设置，确认在同一个终端会话测试。
3. **SSH 失败但 HTTPS Git 成功：**SSH 端口/出口与 HTTPS 是不同路径；可按 GitHub 官方指南选择有授权的 HTTPS 方式，不要随意改防火墙。
4. **包管理器失败：**先核对官方仓库 URL、证书和锁文件；用临时环境变量诊断，避免污染全局配置。
5. **IDE 插件失败：**核对插件进程与其网络权限，不假定集成终端代理设置自动覆盖插件。
6. **Docker 镜像失败：**检查是 Docker Desktop、dockerd，还是容器内应用；三者设置不同。

## 五、Docker 与容器

- **Docker Desktop：**到 Desktop 官方设置中配置代理，不要套用 Linux `daemon.json` 方案。
- **Linux Engine：**参考 [Docker daemon proxy](https://docs.docker.com/engine/daemon/proxy/)，使用经过批准的代理、按文档重启服务；会影响拉镜像等操作，生产环境需变更窗口。
- **容器内：**运行期需要单独设计必要的环境变量和 `NO_PROXY`；`localhost` 在容器内通常指容器自身，**不等于宿主机**。
- **日志：**代理 URL 如果包含凭据，不在命令行截图和 issue 中公开；应优先使用组织密钥管理。

## 六、收工清理与回滚

临时命令如 `HTTPS_PROXY=... command` 仅影响该命令。若之前在 shell 执行过 `export`，可在确认不是企业必须配置后运行：

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
```

不要无条件删除 `NO_PROXY`，它可能关系内网服务。若你修改了永久 Git 配置，先执行 `git config --global --get-regexp '^http.*proxy'` 人工查看并脱敏后确认，再做定点恢复。不得运行陌生人提供的“一键清空全部网络”脚本。

**完成标准：**至少分别验证浏览器、终端、IDE（如使用）、Docker（如使用）四个执行面；每一个写明成功/失败、记录证据、回滚动作。模板见 [开发工作流验收表](../templates/开发工作流验收表.md)。
