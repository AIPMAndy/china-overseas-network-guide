#!/usr/bin/env python3
"""把仓库 Markdown 生成一个无外部依赖的可离线阅读 index.html。
构建依赖：mistune>=3,<4；产物本身无依赖。
"""
from pathlib import Path
import html
import re
from urllib.parse import unquote

try:
    import mistune
except ImportError as exc:
    raise SystemExit("缺少构建依赖。先运行：python3 -m pip install -r requirements-build.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
md = mistune.create_markdown(plugins=["table", "strikethrough", "task_lists", "url"])
chapters = sorted((ROOT / "docs").glob("*.md"))
chapters = [ROOT / "README.md"] + chapters

# 重定向各个 MD 里的相对链接，使 index.html 内可以跳到对应章节。
labels = {p.name: f"chapter-{i:02d}" for i, p in enumerate(chapters)}
sections = []
navs = []
for i, path in enumerate(chapters):
    content = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", content, re.M)
    title = (title_match.group(1) if title_match else path.stem).strip()
    markup = md(content)
    def remap(match):
        raw = html.unescape(match.group(1))
        decoded = unquote(raw)
        if decoded in ("index.html", "./index.html"):
            return 'href="#chapter-00"'
        if decoded.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        file_name = Path(decoded.split("#")[0]).name
        if file_name in labels:
            return f'href="#{labels[file_name]}"'
        if decoded.startswith("../") and path.parent.name == "docs":
            return f'href="{html.escape(decoded[3:], quote=True)}"'
        return match.group(0)
    markup = re.sub(r'href="([^"]+)"', remap, markup)
    sections.append(f'<section class="chapter" id="chapter-{i:02d}" data-search="{html.escape(title)}"><div class="chapter-index">{i:02d} / {len(chapters)-1:02d}</div>{markup}</section>')
    navs.append(f'<a class="navlink" href="#chapter-{i:02d}"><span class="navnum">{i:02d}</span><span>{html.escape(title)}</span></a>')

html_text = r'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="在中国海外网络稳定使用保姆级教程：12类网络模式、36章实操、30天使用策略、故障排查、主备演练、隐私和安全。">
<title>在中国海外网络稳定使用保姆级教程 · AI 酋长 Andy</title>
<style>
:root{--bg:#f7f8fa;--surface:#fff;--ink:#161a20;--muted:#606a7b;--line:#e7ebf0;--accent:#2563eb;--pale:#eff5ff;--shadow:0 24px 65px rgba(20,34,56,.045)}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--surface:#151a21;--ink:#e8edf6;--muted:#a1acbd;--line:#2b3543;--accent:#8ab4ff;--pale:#1b2c43;--shadow:none}}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:15px/1.85 -apple-system,BlinkMacSystemFont,"SF Pro Display","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink)}a{color:var(--accent);text-underline-offset:3px}button,input{font:inherit}header{padding:68px max(24px,calc((100vw - 1180px)/2));background:var(--surface);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:.15em;font-weight:760;color:var(--accent)}.hero h1{font-size:clamp(34px,5.5vw,66px);line-height:1.16;letter-spacing:-.06em;margin:20px 0 18px;max-width:890px}.hero p{font-size:17px;color:var(--muted);margin:0;max-width:760px}.pillset{display:flex;gap:8px;flex-wrap:wrap;margin-top:27px}.pill{border:1px solid var(--line);border-radius:50px;padding:4px 13px;font-size:12px;color:var(--muted)}.shell{max-width:1290px;margin:auto;display:grid;grid-template-columns:270px minmax(0,1fr);gap:36px;padding:35px 24px 80px}.sidebar{position:sticky;top:20px;align-self:start;max-height:calc(100vh - 40px);overflow:auto;padding:12px 0;scrollbar-width:thin}.sidetitle{color:var(--muted);font-size:11px;font-weight:800;letter-spacing:.14em;padding:9px 14px}.search{width:calc(100% - 24px);margin:0 12px 15px;border:1px solid var(--line);border-radius:13px;background:var(--surface);color:var(--ink);padding:10px 12px;outline:none}.search:focus{border-color:var(--accent)}.navlink{display:flex;gap:9px;text-decoration:none;color:var(--muted);line-height:1.38;font-size:12px;border-radius:9px;margin:2px 6px;padding:10px 9px}.navlink:hover,.navlink.active{background:var(--pale);color:var(--accent)}.navnum{font-size:10px;font-weight:700;min-width:18px;color:var(--accent)}main{min-width:0}.chapter{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:42px clamp(18px,4vw,62px);margin-bottom:28px;box-shadow:var(--shadow);scroll-margin-top:20px;overflow-wrap:anywhere}.chapter-index{font:700 11px/1.2 system-ui;letter-spacing:.16em;color:var(--accent)}.chapter h1{font-size:clamp(26px,3.4vw,37px);line-height:1.35;letter-spacing:-.045em;margin:16px 0 24px}.chapter h2{font-size:21px;line-height:1.4;letter-spacing:-.03em;margin:38px 0 12px}.chapter h3{font-size:17px;margin:24px 0 8px}.chapter p{margin:12px 0}.chapter blockquote{margin:20px 0;padding:12px 20px;border-left:3px solid var(--accent);background:var(--pale);border-radius:0 10px 10px 0}.chapter table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;font-size:13px;margin:16px 0}.chapter th,.chapter td{border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;min-width:90px;vertical-align:top}.chapter th{background:var(--pale)}.chapter pre{background:var(--bg);border:1px solid var(--line);padding:17px;overflow:auto;border-radius:10px;font-size:12px;line-height:1.6}.chapter code{font:12px ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-word;background:var(--pale);border-radius:4px;padding:2px 5px}.chapter pre code{background:none;padding:0;word-break:normal}.chapter li{margin:7px 0}.chapter strong{font-weight:750}.chapter ol,.chapter ul{padding-left:22px}.off{display:none!important}.site-nav{display:flex;flex-wrap:wrap;gap:20px;padding:16px max(24px,calc((100vw - 1180px)/2));background:var(--surface);border-bottom:1px solid var(--line)}.site-nav a{font-size:13px;text-decoration:none}.end{text-align:center;padding:20px;color:var(--muted);font-size:12px}.top{position:fixed;right:22px;bottom:22px;padding:9px 15px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;box-shadow:var(--shadow);cursor:pointer}#status{color:var(--muted);font-size:12px;padding:0 12px}#progress{height:3px;background:var(--accent);position:fixed;top:0;left:0;width:0;z-index:20;transition:width .1s}
@media(max-width:850px){header{padding:48px 22px}.shell{display:block;padding:15px 12px 65px}.sidebar{position:relative;top:auto;max-height:none;padding:12px 0 22px}.navs{display:flex;overflow-x:auto;scrollbar-width:thin;white-space:nowrap}.navlink{flex:0 0 auto;max-width:240px}.navlink span:last-child{overflow:hidden;text-overflow:ellipsis}.chapter{padding:24px 20px;margin-bottom:12px;border-radius:12px}.top{bottom:14px;right:14px}}
@media print{header{padding:20px}.sidebar,#progress,.top{display:none}.shell{display:block;padding:0}.chapter{box-shadow:none;break-before:page;border:0;padding:10px}}
</style></head><body><div id="progress"></div><nav class="site-nav" aria-label="主导航"><a href="#chapter-00">开始阅读</a><a href="https://github.com/AIPMAndy/china-overseas-network-guide" target="_blank" rel="noopener noreferrer">GitHub</a><a href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">个人官网 ↗</a></nav><header class="hero"><div class="eyebrow">OPEN-SOURCE FIELD GUIDE / VERSION 3.0</div><h1>在中国海外网络稳定使用<br>保姆级教程</h1><p>覆盖商业 VPN、代理订阅、自建 VPS、国际漫游、企业专线、私有组网、Tor 等 12 类模式；从零基础配置，到分设备使用、真实业务验收、30天执行、主备演练、安全和应急回滚。无永久稳定承诺。</p><div class="pillset"><span class="pill">AI 酋长 Andy</span><span class="pill">免费开源</span><span class="pill">36 篇实操章节</span><span class="pill">2026-10-12 核对</span></div></header>
<div class="shell"><aside class="sidebar"><div class="sidetitle">CHAPTERS / 目录</div><input id="search" class="search" type="search" placeholder="搜索内容，例如 DNS、iPhone、密钥" aria-label="搜索教程"><div id="status"></div><nav class="navs">__NAV__</nav></aside><main id="content">__CHAPTERS__<footer class="end">AI 酋长 Andy · 36 章 · 12 类模式 · 以合法授权与实测为前提 · MIT License<br>微信 <strong>AIPMAndy</strong> · <a href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">个人官网</a><br>求职、职业发展与 AI 应用咨询可通过微信联系，咨询可选，不影响免费阅读。</footer></main></div><button id="top" class="top" type="button">回顶部 ↑</button>
<script>
(()=>{const input=document.getElementById('search');const chapters=[...document.querySelectorAll('.chapter')];const navs=[...document.querySelectorAll('.navlink')];const progress=document.getElementById('progress');const norm=s=>(s||'').toLocaleLowerCase();const hay=chapters.map(el=>norm(el.textContent));function filter(){const q=norm(input.value.trim());let n=0;chapters.forEach((el,i)=>{const match=!q||hay[i].includes(q);el.classList.toggle('off',!match);navs[i].classList.toggle('off',!match);n+=+match;});document.getElementById('status').textContent=q?`找到 ${n} 个章节（按标题与全文匹配）`:'';}input.addEventListener('input',filter);const sync=()=>{const total=document.documentElement.scrollHeight-innerHeight;progress.style.width=(total>0?Math.min(100,Math.max(0,scrollY/total*100)):0)+'%';let found=0;for(let i=0;i<chapters.length;i++){if(!chapters[i].classList.contains('off')&&chapters[i].getBoundingClientRect().top<=180)found=i;}navs.forEach((el,i)=>el.classList.toggle('active',i===found));};window.addEventListener('scroll',sync,{passive:true});document.getElementById('top').onclick=()=>scrollTo({top:0,behavior:'smooth'});sync();})();
</script></body></html>'''
html_text = html_text.replace("__NAV__", "\n".join(navs)).replace("__CHAPTERS__", "\n".join(sections))
(ROOT / "index.html").write_text(html_text, encoding="utf-8")
print("index.html generated, chapters:", len(chapters), "bytes:", len(html_text.encode("utf-8")))
