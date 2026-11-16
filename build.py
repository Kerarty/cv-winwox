#!/usr/bin/env python3
"""Сборка cv-winwox: инлайнит шрифты и скриншоты в один index.html.
Запуск: python build.py"""
import base64
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

def b64(rel):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return base64.b64encode(f.read()).decode()

REPL = {
    '{{FONT_GOLOS_CYR}}':  b64('assets/fonts/golos-cyr.woff2'),
    '{{FONT_GOLOS_LAT}}':  b64('assets/fonts/golos-lat.woff2'),
    '{{FONT_MPLUS_CYR}}':  b64('assets/fonts/mplus-800-cyr.woff2'),
    '{{FONT_MPLUS_LAT}}':  b64('assets/fonts/mplus-800-lat.woff2'),
    '{{IMG_ECHO_TITLE}}':  b64('assets/shots/echoloop-title.webp'),
    '{{IMG_ECHO_GATE}}':   b64('assets/shots/echo-and-gate.webp'),
    '{{IMG_GATES}}':       b64('assets/shots/gates.webp'),
    '{{IMG_KITTY}}':       b64('assets/shots/kitty.webp'),
}

with open(os.path.join(ROOT, 'src', 'index.template.html'), encoding='utf-8') as f:
    html = f.read()

import re

for k, v in REPL.items():
    if k not in html:
        raise SystemExit(f'!! плейсхолдер не найден в шаблоне: {k}')
    html = html.replace(k, v)

leftover = re.findall(r'\{\{[A-Z_]+\}\}', html)
if leftover:
    raise SystemExit('!! в шаблоне остались плейсхолдеры: ' + ', '.join(leftover))

out = os.path.join(ROOT, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK -> index.html ({os.path.getsize(out)/1024:.0f} КБ)')
