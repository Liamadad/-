import json, os
os.makedirs('out', exist_ok=True); os.makedirs('site', exist_ok=True)
data = open('words.json', encoding='utf-8').read()
app = open('app.html', encoding='utf-8').read().replace('/*__DATA__*/null', data)
open('out/danci.html', 'w', encoding='utf-8').write(app)
head = '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
title_end = app.index('</title>') + len('</title>')
doc = head + app[:title_end] + '\n</head>\n<body>\n' + app[title_end:] + '\n</body>\n</html>\n'
open('site/index.html', 'w', encoding='utf-8').write(doc)
print(len(app), len(doc))

plan = open('plan.html', encoding='utf-8').read()
open('out/plan.html', 'w', encoding='utf-8').write(plan)
t = plan.index('</title>') + len('</title>')
open('site/plan.html', 'w', encoding='utf-8').write(head + plan[:t] + '\n</head>\n<body>\n' + plan[t:] + '\n</body>\n</html>\n')
