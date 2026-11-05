#!/usr/bin/env python3
"""tools/ 内のHTMLから tools/list.json を作り直す。各HTMLの <title> と
<meta name="mini-category"> / <meta name="mini-desc"> を読む。v は内容のハッシュ。"""
import hashlib, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent / "tools"
SW = '<script data-mini-sw>(function(){if(!/\\/tools\\/[^/]*$/.test(location.pathname))return;var root=location.pathname.replace(/tools\\/[^/]*$/,"");if("serviceWorker"in navigator)navigator.serviceWorker.register(root+"sw.js").catch(function(){});if(navigator.standalone===true&&window.top===window){addEventListener("DOMContentLoaded",function(){var a=document.createElement("a");a.href=root;a.textContent="\\u2039 ミニ置き場";a.style.cssText="position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:2147483647;background:rgba(20,24,32,.88);color:#fff;font:600 14px/1 system-ui,sans-serif;padding:10px 14px;border-radius:20px;text-decoration:none;box-shadow:0 2px 10px rgba(0,0,0,.3)";document.body.appendChild(a)})}})()</script>'
out = []
for f in sorted(root.glob("*.htm*")):
    s = f.read_text(encoding="utf-8", errors="replace")
    s2 = re.sub(r"<script data-mini-sw>.*?</script>", lambda m: SW, s, flags=re.S)
    if s2 != s:
        s = s2; f.write_text(s, encoding="utf-8")
    if "data-mini-sw" not in s and re.search(r"</body>", s, re.I):
        i = [m.start() for m in re.finditer(r"</body>", s, re.I)][-1]
        s = s[:i] + SW + "\n" + s[i:]
        f.write_text(s, encoding="utf-8")
    m = lambda n: (re.search(r'<meta\s+name=["\']%s["\']\s+content=["\']([^"\']*)' % n, s, re.I) or [None, ""])[1].strip()
    t = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
    out.append({"file": f.name,
                "title": m("mini-title") or (re.sub(r"\s+", " ", t.group(1)).strip() if t else f.stem),
                "cat": m("mini-category") or "other",
                "desc": m("mini-desc"),
                "v": hashlib.sha1(s.encode()).hexdigest()[:10]})
(root / "list.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "tools")
