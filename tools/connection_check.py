#!/usr/bin/env python3
"""只读的本机 DNS 和 HTTPS 连通性诊断。
不会读取 VPN 配置/私钥、不会向作者上报；访问所列公开测试域名本身会形成普通网络请求。
本测试不证明任何线路的合法性、安全性、地理位置或稳定性。
"""
import datetime as dt
import socket
import ssl
import time
from urllib.parse import urlsplit

TARGETS = [
    ("基础 HTTPS", "https://example.com"),
    ("代码托管", "https://github.com"),
    ("百科网站", "https://www.wikipedia.org"),
]
TIMEOUT = 6


def check(url):
    host = urlsplit(url).hostname
    start = time.monotonic()
    try:
        # 仅 DNS 解析，不输出真实 IP；下面的直接 socket 测试不遵循所有系统代理配置。
        socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        dns_status = "OK"
    except Exception as exc:
        return ("FAIL", "DNS:" + type(exc).__name__, round(time.monotonic() - start, 2))
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=host) as conn:
                conn.settimeout(TIMEOUT)
                conn.sendall((f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n").encode())
                line = conn.recv(160).split(b"\r\n", 1)[0].decode("ascii", "replace")
                if line.startswith("HTTP/"):
                    return ("OK", "DNS=" + dns_status + " TLS=OK " + line[:45], round(time.monotonic() - start, 2))
                return ("FAIL", "TLS=OK but unexpected HTTP response", round(time.monotonic() - start, 2))
    except Exception as exc:
        return ("FAIL", "HTTPS:" + type(exc).__name__, round(time.monotonic() - start, 2))


def main():
    print("本机诊断时间：" + dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("注意：直接 TCP/TLS 测试通常不经过 HTTP 系统代理。失败不等于受控 VPN/代理无效。")
    print("请求目标为 example.com、github.com、www.wikipedia.org；这会向各站发送普通访问请求。\n")
    for label, url in TARGETS:
        status, detail, seconds = check(url)
        print(f"{label:8} {status:4} {seconds:5.2f}s | {detail}")
    print("\n若使用代理类客户端，请额外在实际工作 App 中核验，参考 docs/06-如何判定稳定.md。")


if __name__ == "__main__":
    main()
