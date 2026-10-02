"""Wrap app.html (artifact-style fragment) into a full HTML document: local.html.

app.html deliberately has no <!doctype>/<html>/<head>/<body>: the hosting platform
adds that skeleton. This script adds an equivalent skeleton so the app also works
when the demo folder is served locally (python -m http.server) and in Playwright.

Usage:  python build_local.py        (run it after every change to app.html)
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "app.html"
OUT = HERE / "local.html"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
/* same small reset the hosting platform provides */
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f8f8f6}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"


def main() -> None:
    body = SRC.read_text(encoding="utf-8")
    low = body.lstrip().lower()
    if low.startswith("<!doctype") or low.startswith("<html"):
        raise SystemExit("app.html must stay a fragment (no <!doctype>/<html>): the platform adds the skeleton")
    OUT.write_text(HEAD + body + TAIL, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.name} ({OUT.stat().st_size / 1024:.0f} KB) from {SRC.name}")


if __name__ == "__main__":
    main()
