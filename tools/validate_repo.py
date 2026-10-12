#!/usr/bin/env python3
"""静态审核：链接路径、文档完整性及有限的明文凭据风险检查。
启发式规则可能有误报和漏报，绝不能当作完整 Secret Scanning。
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "docs").glob("*.md"))
MD_FILES = [ROOT / "README.md", ROOT / "SOURCES.md", ROOT / "AUDIT.md", ROOT / "AUDIT_V3.md", ROOT / "RESEARCH_LOG.md", ROOT / "SECURITY.md", ROOT / "CONTRIBUTING.md"] + DOCS + list((ROOT / "templates").glob("*.md"))
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REAL_IP = re.compile(r"(?<![0-9])(?:\d{1,3}\.){3}\d{1,3}(?![0-9])")
PRIVATE = [re.compile(x, re.I) for x in [
    r"-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----",
    r"(?:ss|trojan|vless|vmess|hysteria2)://[^\s)`]+",
    r"(?:^|\s)sk-[A-Za-z0-9]{18,}",
    r"(?:password|passwd|token|secret|api_key)\s*[=:]\s*['\"]?[^\s'\"]{12,}",
]]
ALLOW_IP_PREFIX = ("203.0.113.", "198.51.100.", "192.0.2.", "127.", "0.")

def main():
    issues = []
    if len(DOCS) < 24:
        issues.append("章节少于 24 个")
    for md in MD_FILES:
        txt = md.read_text(encoding="utf-8")
        if not txt.strip():
            issues.append(f"空文件：{md.relative_to(ROOT)}")
        for target in LINK.findall(txt):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            dest = (md.parent / unquote(target.split("#")[0])).resolve()
            if not dest.exists():
                issues.append(f"本地链接不可用：{md.relative_to(ROOT)} → {target}")
        for i, line in enumerate(txt.splitlines(), 1):
            # 仅检查可能暴露的公网 IPv4；不处理构成文档解释的协议前缀。
            for address in REAL_IP.findall(line):
                if not address.startswith(ALLOW_IP_PREFIX):
                    issues.append(f"可能含真实 IPv4：{md.relative_to(ROOT)}:{i} {address}")
            for pattern in PRIVATE:
                if pattern.search(line):
                    # `ss://` 等协议描述的代码片段常属文本说明，用于识别可疑明文凭据。
                    issues.append(f"疑似明文凭据：{md.relative_to(ROOT)}:{i}（人工复核）")
    if not (ROOT / "index.html").exists():
        issues.append("index.html 尚未生成")
    print(f"审核文档 {len(MD_FILES)} 个，其中教程 {len(DOCS)} 篇")
    if issues:
        print("\n检查结果：\n- " + "\n- ".join(issues))
        return 1
    print("本地链接有效；未检出规则覆盖范围内的明显凭据泄露。请仍作人工审查。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
