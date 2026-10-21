# ミニ置き場

`index.html` が置き場本体。`tools/` に置いたHTMLは全端末に自動で届く（共通の棚）。

ツールを足すとき:
1. HTMLの `<head>` に `<meta name="mini-category" content="clinical|learn">` と `<meta name="mini-desc" content="ひとこと">` を入れる
2. `tools/` に置く
3. `python3 scripts/build_list.py` で `tools/list.json` を作り直してpush
