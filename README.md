# 本科 Python 代码归档

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

本科阶段的课程作业、练习代码与研究项目脚本，按用途分为五大类，可直接克隆运行。

> 数据不随仓库分发。缺数据时先跑 `python tools/simulate_data.py --dataset all`
> 生成结构一致的合成数据，详见 [`04_resources/data/DATA.md`](04_resources/data/DATA.md)。

## 目录结构

```
python-learning-archive/
├── 01_coursework/                    课程作业（可提交、有明确题目）
│   ├── data-analysis-practice/       数据分析实训：爬虫 + pandas + pyecharts
│   │   ├── classwork_01_maoyan_top100/   猫眼 Top100 电影分析
│   │   ├── classwork_02_weibo_hotsearch/ 微博热搜可视化
│   │   ├── classwork_03_dangdang/        当当网图书价格对比
│   │   └── day01 ~ day07/                课堂讲义与逐日练习
│   ├── data-warehouse/               数据仓库实训：关联规则 / 客户价值 / 信用卡
│   ├── machine-learning/             机器学习三天讲义：sklearn 特征工程、回归、聚类
│   └── text-mining/                  文本分析与挖掘课程：BERT、SentenceTransformer、
│                                     BERTopic、LangChain、方面级情感分析
├── 02_practice/                      零散练习（非作业，代码试验）
│   ├── deep-learning/                TensorFlow 1.x 图与会话机制
│   ├── jupyter-notebooks/            PCA / Titanic / 乳腺癌数据集
│   └── visualization/                网约车时段统计、地震数据回归
├── 03_research/                      论文与项目脚本
│   ├── course-review-topic-modeling/ 课程评论文本 → BERTopic 主题建模 + TF-IDF
│   ├── provincial-tourism-lda/       五省旅游政策文本 → jieba + LDA + 共现网络
│   ├── teaching-reform-analysis/     教改论文：评教数据清洗 + 多模态融合模型
│   └── misc-figures/                 论文配图：RFM 三维图、UI 优化效果图
├── 04_resources/                     公共数据集与词典
│   ├── README.md
│   └── data/DATA.md                  数据获取与模拟指南（必读）
├── 99_archive/                       临时/无用文件，保留但不建议使用
├── tools/simulate_data.py            合成数据生成器（缺数据时用它跑通流程）
├── requirements.txt                  核心依赖
├── requirements-nlp.txt              文本/深度学习重型依赖
└── .gitignore
```

## 快速开始

```bash
git clone <仓库地址> && cd python-learning-archive

python -m venv .venv && source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt

# 原始数据不随仓库分发，先生成一份结构一致的合成数据，即可跑通全部示例
python tools/simulate_data.py --dataset all
```

需要跑文本挖掘或深度学习时，再装重型依赖（体积大、耗时长）：

```bash
pip install -r requirements-nlp.txt
```

> `.venv/` 是原机器的虚拟环境（约 1.6 GB），未做备份改动，仍保留在原位置。
> 由于 Python 虚拟环境绑定绝对路径，迁移或移动目录后请重建，不要直接复用。

## 数据与路径

原始数据大多存放在课程平台、桌面目录，**没有随代码归档**。完整的数据来源、获取途径与
合成方案见 **[`04_resources/data/DATA.md`](04_resources/data/DATA.md)**，这里只列速查。

三种拿到数据的方式：

| 方式 | 做法 | 适用 |
|---|---|---|
| 用合成数据 | `python tools/simulate_data.py --dataset all` | 只想跑通流程、验证代码 |
| 放自己的真实数据 | 按环境变量指向你的目录（见下表） | 有原始数据 |
| 重新采集 | 运行对应的爬虫脚本 | 数据公开可抓 |

脚本已改为「环境变量优先 + 项目内相对路径兜底」，按下表设置即可指向你本机的数据：

| 环境变量 | 作用 | 默认值 |
|---|---|---|
| `BERT_MODEL_DIR` | 本地 `bert-base-chinese` 模型目录 | `D:/bert-base-chinese` |
| `TEXTMINING_DATA_DIR` | 文本挖掘课程数据根目录（含「第四章」「第五章」） | 原作者本机路径 |
| `TEXTMINING_OUTPUT_DIR` | 文本挖掘输出目录 | `text-mining/outputs` |
| `COURSE_REVIEW_DATA_DIR` | 课程评论 Excel 所在目录 | `course-review-topic-modeling/data` |
| `COURSE_REVIEW_OUTPUT_DIR` | BERTopic 结果目录 | `course-review-topic-modeling/outputs` |
| `LUO_SOURCE_DIR` | 五省旅游政策 docx/pdf 目录 | 原作者桌面目录 |
| `TEACHING_DATA_DIR` | 评教明细 CSV 目录 | `teaching-reform-analysis/data` |
| `WAREHOUSE_DATA_DIR` | 数据仓库实训 Excel 目录 | `data-warehouse/data` |
| `VIS_DATA_DIR` | 可视化练习 CSV/Excel 目录 | `visualization/data` |
| `SKLEARN_DATA_HOME` | sklearn 数据集缓存目录 | `machine-learning/sklearn_datasets` |
| `WORDCLOUD_FONT` | 词云中文字体文件 | `C:\Windows\Fonts\simhei.ttf` |
| `ZHIPUAI_API_KEY` | 智谱 AI Key（方面级情感分析用） | 无，未设置则拒绝运行 |
| `SITE_LOGIN_NAME` | 爬虫练习站点的登录账号 | 无，未设置则请求不带账号 |
| `SITE_LOGIN_PWD` | 同上，密码 | 无 |
| `SITE_COOKIE` | 同上，浏览器 Cookie | 无 |

示例：

```bash
export TEXTMINING_DATA_DIR="D:/课程资料/文本分析与挖掘"
export BERT_MODEL_DIR="D:/models/bert-base-chinese"
python 01_coursework/text-mining/1023/01_bertopic_basic.py
```

## 运行方式

脚本都是独立入口，直接按路径运行即可：

```bash
# 数据仓库实训：关联规则 / 回归 / 客户价值 / 营销响应
python 01_coursework/data-warehouse/work01_01.py
python 01_coursework/data-warehouse/work02_01.py

# 可视化练习
python 02_practice/visualization/new.py

# 研究项目
python 03_research/course-review-topic-modeling/preprocess_comments.py
python 03_research/provincial-tourism-lda/sichuan.py
```

`03_research` 下的脚本会在同目录生成 `outputs/` 或图片文件，属于预期产物。

## 已验证可运行的脚本

以下脚本在 `python 3.13` + `requirements.txt` 环境下，用 `tools/simulate_data.py`
生成的合成数据实际跑通（退出码 0，产出图表/规则表）：

| 脚本 | 内容 | 产物 |
|---|---|---|
| `data-warehouse/work01_01.py` | Apriori 关联规则 | 规则表（支持度/置信度/提升度） |
| `data-warehouse/work01_02.py` | FP-Growth 关联规则 | 规则表 |
| `data-warehouse/work02_01.py` | 多项式回归（1~5 次） | R²/MAE/MSE 对比 + 拟合图 |
| `data-warehouse/work02_02.py` | 相关性热力图 + 多项式特征 | 热力图 |
| `data-warehouse/work03_01.py` | 决策树营销响应预测 | 准确率/ROC |
| `visualization/new.py` | 网约车小时分布 | `car_trips_by_hour.html` |
| `course-review-topic-modeling/preprocess_comments.py` | 分词 + 去停用词 | 预处理后表格 |
| `provincial-tourism-lda/sichuan.py` | LDA + 共现网络 + pyLDAvis | 主题雷达图、网络图、交互 HTML |

未实测：`zhengli.py`（依赖 xgboost）、`bertopic_pipeline.py`（依赖 torch，
首次运行需下载 sentence-transformers 模型）、`teacher_review_analysis.py`
（依赖 TensorFlow）、`day03/01-王者荣耀.py`（需联网抓图）。

## 已知限制

- 外部数据集缺失，除少数自带数据的脚本外，多数脚本无法在裸克隆后直接跑通，需先准备数据
  （或运行 `tools/simulate_data.py`）。
- `02_practice/visualization/zhengli.py` 原用 `scipy.polyfit`（早已移除），已改为 `numpy.poly1d`。
- `01_coursework/data-analysis-practice/day01/英雄联盟.py` 原本是从交互式终端粘贴的片段，缩进错乱无法执行，已重排为可运行脚本。
- 部分爬虫脚本依赖网页结构，站点改版后会失效；`day05/00-超级鹰.py` 为验证码平台示例，需要自备账号。
- 深度学习脚本基于 TensorFlow 1.x 兼容模式（`tf.compat.v1`），需安装 TF 2.x 并禁用 v2 行为。
- `pyLDAvis 3.4` 与 `numpy>=2` 存在兼容问题：PCoA 会返回复数特征值，保存 HTML 时报
  `complex128 is not JSON serializable`。已在 `provincial-tourism-lda/config.py` 中打补丁
  （改用 `np.linalg.eigh`），无需降级 numpy。
- 王者荣耀皮肤图（约 37 MB）未入库，`day03/01-王者荣耀.py` 可重新抓取；版权归游戏厂商。

## 整理说明

本仓库内容整理自本科阶段的本地工作目录，共完成：

- 按用途重组为 `01_coursework / 02_practice / 03_research` 三类，`my paper` 中混杂的
  四个不相关项目拆分为独立子项目；
- 重命名 34 个无语义或无序号的文件（如 `work1-1.py` → `work01_01.py`）；
- 60+ 处硬编码绝对路径改为「环境变量优先 + 相对路径兜底」，新增 4 个 `config.py`；
- 移除明文 API Key、登录手机号、密码与 Cookie（改为 `ZHIPUAI_API_KEY`、`SITE_*`）；
- 修复 6 处导致脚本无法运行的缺陷（详见「已知限制」与 `git log`）。

原始快照与逐项变更对照表由作者本地留存，未随仓库公开。
