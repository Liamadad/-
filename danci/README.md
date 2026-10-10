# 每日单词本

一个手机网页，每天列出要默写、要认识和要复习的英文单词，从 2026 年 10 月 12 日到 2027 年底。另附一页给家长看的计划图。

- `site/index.html`：每日单词本，独立文件，不依赖任何外部字体或脚本，放到任何静态网站空间都能打开。
- `site/plan.html`：计划图。
- `DEPLOY_PROMPT.md`：发布到 GitHub Pages 的操作说明，可以直接交给有电脑操作能力的助手执行。

## 计划

| 阶段 | 周次 | 日期 | 每个学习日新词 |
|---|---|---|---|
| 打基础 | 1–12 | 2026-10-12 – 2027-01-03 | 10 默写 + 20 认识 |
| 扩词汇 | 13–44 | 2027-01-04 – 08-15 | 10 默写 + 20 认识 |
| 巩固 | 45–50 | 2027-08-16 – 09-26 | 5 默写 + 10 认识 |
| 冲刺 | 51–55 | 2027-09-27 – 10-31 | 只复习 |
| 考后 | 56–64 | 2027-11-01 – 2028-01-02 | 5 默写 + 10 认识 |

- 周一到周五学新词；每个词在学完后的第 1、2、4、7、15、30 个学习日复习，网页自动列出。
- 周六周测，周日复习和补考；每月最后一个周六认识词改为从学过的所有词里随机 50 个。
- 合计：默写 2,575 个，认识 5,150 个。

## 网页功能

2026-10-10 起换成新设计（「单词卡」风格，用 Oil UI Pro 从零设计，过程和取舍见 `redesign/DESIGN_NOTES.md`；旧版源码存档在 `redesign/app-v1.html`）。

- 左右箭头切换日期，默认显示手机当天的日期（香港时间）。刷新时回到刚才那一天和那张卡，重新打开链接一律回到今天。
- 几叠词：平日是复习 / 默写 / 认识，周末是本周默写 / 本周认识。每叠可以用「清单」看全部，也可以用「卡片」一张一张翻着自测。
- 「开始检查」（周六是「开始周测」，周日是「周日补考」）：先听写默写词（自动读音），再对答案、点出写错的；然后考认识词，按「会 / 不会」；最后显示对了几个、过没过关，可以只重考错的。学习日的检查还会从当天的复习词里随机抽 10 个（3 个默写 + 7 个认识，对 8 个过关），和新词混在一起考，结果单独算。每按一次都重新随机抽题、打乱顺序。计数只在这一次检查里有效，不保存。
- 喇叭：英式发音，优先用有道词典的真人录音（香港和内地都能访问），加载失败时改用手机自带的语音。
- 「添加到主屏幕」：`pwa/` 里有图标、`manifest.webmanifest` 和 `sw.js`，`assemble.py` 会把它们复制到 `site/`。加到主屏幕后没网也能打开，但发音仍要联网。

## 词表来源

- 学科词（2026-10-10 加入）：剑桥 IGCSE Economics 0455、Physics 0625、Mathematics 0580 考纲里的术语，以及考试指令词（describe、explain、calculate 等），整理在 `subjects/*.json`。每个词标了默写或认识、重要程度 1–3 和考纲章节；第 3 档（冷门）一律只要求认识。中文释义按学科写（current → 电流），释义后面注明科目，比如（物理）。合并和排序的逻辑在 `subjects.py`。
- 默写第一阶段：指令词、三科第 1 档词和 AWL 第 1 子表按比例穿插；再到三科第 2 档词和 AWL 第 2–4 子表；然后是 AWL 第 5–10 子表。AWL 是 Academic Word List 的 570 个词头（Coxhead, 2000），逐个核对过存在于词典中。
- 认识：New General Service List（Browne, 2013）第 501 名以后的词，取自 PyPI 包 `ngsl`；之后接 ECDICT 中标为雅思或托福的词，按 COCA 与 BNC 词频平均排名排序。三科只需看懂的词按重要程度穿插进去：第 1 档放在 NGSL 前 500 个里，第 2 档放在 NGSL 其余部分里，第 3 档放在雅思托福词里。每天的量不变，所以最后一批最不常用的雅思托福词被挤出计划。
- 默写第二阶段：认识列表里出现过的 5 个字母以上的词，按出现顺序升级为默写，保证每个词先学认识、后学默写。
- 中文释义和音标：ECDICT（skywind3000，MIT 许可），自动截取前两个词性、每个词性最多三个义项。

NGSL 以 CC BY-SA 4.0 发布，由它派生的词表数据（`words.json` 中的相应部分）同样按 CC BY-SA 4.0 提供。

## 重新生成

源数据不提交，放在 `dl/`（或用环境变量 `DANCI_DL` 指定）：

```bash
mkdir -p dl/ngslpkg
curl -L -o dl/ecdict.csv https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
pip download ngsl==1.41 --no-deps --no-binary :all: -d dl/ngslpkg && tar -xzf dl/ngslpkg/ngsl-1.41.tar.gz -C dl/ngslpkg

python3 build.py      # 生成 words.json
python3 assemble.py   # 把 words.json 嵌进 app.html，输出 site/（网页、计划图、图标和离线文件，共 8 个，要一起上传）以及 out/ 下的片段版
```

修改日程改 `app.html` 里的 `START` 和 `PLAN`；修改每天词量还要同步改 `build.py` 里的 `SPELL_TOTAL` 和 `REC_TOTAL`。

## 测试

```bash
python3 assemble.py
node tests/test.js                                   # 日程逻辑：所有词都排进日程、先认识后默写、日期映射
NODE_PATH=$(npm root -g) node tests/ftest.js         # 页面功能（需要 Playwright）
NODE_PATH=$(npm root -g) node tests/ftest2.js        # 遮住按钮按词的类型遮对应的一边
NODE_PATH=$(npm root -g) node tests/shot3.js         # 375px 宽度下按钮不小于 44px、无横向滚动（截图写入 shots/）
```
