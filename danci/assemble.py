import json, os
os.makedirs('out', exist_ok=True); os.makedirs('site', exist_ok=True)
data = open('words.json', encoding='utf-8').read()
app = open('app.html', encoding='utf-8').read().replace('/*__DATA__*/null', data)
open('out/danci.html', 'w', encoding='utf-8').write(app)
head = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#EEF1F5" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#11151B" media="(prefers-color-scheme: dark)">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" type="image/png" href="icon-192.png">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')
title_end = app.index('</title>') + len('</title>')
doc = head + app[:title_end] + '\n</head>\n<body>\n' + app[title_end:] + '\n</body>\n</html>\n'
open('site/index.html', 'w', encoding='utf-8').write(doc)
print(len(app), len(doc))

plan = open('plan.html', encoding='utf-8').read()
open('out/plan.html', 'w', encoding='utf-8').write(plan)
t = plan.index('</title>') + len('</title>')
open('site/plan.html', 'w', encoding='utf-8').write(head + plan[:t] + '\n</head>\n<body>\n' + plan[t:] + '\n</body>\n</html>\n')

# 「添加到主屏幕」: icon, app manifest and the offline worker go next to the pages
import shutil
for f in os.listdir('pwa'):
    shutil.copy(os.path.join('pwa', f), os.path.join('site', f))
