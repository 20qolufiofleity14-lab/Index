#!/usr/bin/env python3
"""tools/ 内のHTMLから tools/list.json を作り直す。各HTMLの <title> と
<meta name="mini-category"> / <meta name="mini-desc"> を読む。v は内容のハッシュ。"""
import hashlib, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent / "tools"
out = []
for f in sorted(root.glob("*.htm*")):
    s = f.read_text(encoding="utf-8", errors="replace")
    m = lambda n: (re.search(r'<meta\s+name=["\']%s["\']\s+content=["\']([^"\']*)' % n, s, re.I) or [None, ""])[1].strip()
    t = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
    out.append({"file": f.name,
                "title": re.sub(r"\s+", " ", t.group(1)).strip() if t else f.stem,
                "cat": m("mini-category") or "other",
                "desc": m("mini-desc"),
                "v": hashlib.sha1(s.encode()).hexdigest()[:10]})
(root / "list.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "tools")
