# Build the redesigned page next to the live one, without touching ../site/:
# site2/index.html (full page) and out/danci.html (fragment, for ../tests/test.js run from this folder)
import os
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, 'site2'), exist_ok=True); os.makedirs(os.path.join(here, 'out'), exist_ok=True)
data = open(os.path.join(here, '..', 'words.json'), encoding='utf-8').read()
app = open(os.path.join(here, 'app2.html'), encoding='utf-8').read().replace('/*__DATA__*/null', data)
open(os.path.join(here, 'out', 'danci.html'), 'w', encoding='utf-8').write(app)
head = '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#EEF1F5">\n'
t = app.index('</title>') + len('</title>')
open(os.path.join(here, 'site2', 'index.html'), 'w', encoding='utf-8').write(head + app[:t] + '\n</head>\n<body>\n' + app[t:] + '\n</body>\n</html>\n')
print('ok', len(app))
