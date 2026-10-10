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

- 左右箭头切换日期，默认显示今天。
- 「遮住」：默写词盖住英文，认识词盖住中文；点一行看答案。
- 「打乱顺序」：检查和自测时用，切换遮住时顺序不变。
- 喇叭：英式发音，优先用有道词典音频（香港和内地可访问），失败时改用手机自带语音。

## 词表来源

- 默写第一阶段：Academic Word List 的 570 个词头（Coxhead, 2000），按子表顺序。词头按标准词表整理，逐个核对过存在于词典中。
- 认识：New General Service List（Browne, 2013）第 501 名以后的词，取自 PyPI 包 `ngsl`；之后接 ECDICT 中标为雅思或托福的词，按 COCA 与 BNC 词频平均排名排序。
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
python3 assemble.py   # 把 words.json 嵌进 app.html，输出 site/index.html、site/plan.html（以及 out/ 下的片段版）
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
