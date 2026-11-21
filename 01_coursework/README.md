# 01_coursework · 课程作业

带明确题目、可提交的课程实训练习。按课程分成四个子项目，彼此独立。

## data-analysis-practice — 数据分析实训

爬虫 → 数据清洗 → 可视化（pandas + pyecharts + matplotlib）。

| 子目录 | 内容 | 入口 |
|---|---|---|
| `day01` ~ `day07` | 逐日讲义：requests / bs4 / selenium / pandas / 图表 | 各目录下的 `.py`，按编号顺序 |
| `classwork_01_maoyan_top100` | 猫眼 Top100 电影：评分分布、上映时间、票房 | `plot_movie_count_bar.py` 等 |
| `classwork_02_weibo_hotsearch` | 微博热搜：热度分布、分类占比 | `weibo_charts_collection.py` |
| `classwork_03_dangdang` | 当当网图书价格对比 | `dangdang_stacked_bar.py` |

班级作业的输出 CSV/HTML 已随目录保存，可直接查看结果；重跑需要原始采集数据。

## data-warehouse — 数据仓库实训

| 脚本 | 主题 |
|---|---|
| `work01_01.py` / `work01_02.py` | Apriori 关联规则（金融产品、中医辨证） |
| `work02_01.py` / `work02_02.py` | 行业收入统计、客户价值分群 |
| `work03_01.py` / `work03_02.py` | 信用卡精准营销、交易数据分析 |
| `work04_*` ~ `work06_*` | SQL / ETL / 指标计算练习 |

数据放在 `data/`，清单见该目录 README。

## machine-learning — 机器学习讲义

- `day01_machine_learning.py`：sklearn 数据集、特征抽取、归一化、PCA、相关系数
- `day02_machine_learning.py`：KNN / 朴素贝叶斯 / 决策树 / 随机森林、网格搜索
- `day03_machine_learning.py`：回归、岭回归（产出 `my_ridge.pkl`）

`dating.txt`、`factor_returns.csv` 为随讲义附带的小数据集，开箱可跑。
依赖 `snownlp`（day01 的中文分词增强），未装时会导入失败。

## text-mining — 文本分析与挖掘

按上课日期组织，属于课堂跟练：

| 目录 | 主题 |
|---|---|
| `1021/` | BERT 输入构造：单句、句对、多句、批量、流式 |
| `1023/` | SentenceTransformer 句向量、BERTopic 入门、npy/pt 存取 |
| `1028/` | LangChain 链式调用、BERTopic 参数与可视化、停用词处理 |
| `1104/` | 方面级情感分析 |
| `bert_topic_assignment.py` | 个人作业：TF-IDF + LDA + 词云（自带 `《人工智能导论》评论（作业）.xls`） |
| `zhipu_scenic_comment_analysis.py` | 小组作业：调用智谱 API 做景区评论方面级情感分析 |

### 运行前

```bash
export BERT_MODEL_DIR="D:/models/bert-base-chinese"        # 1021/1023/1028 需要
export TEXTMINING_DATA_DIR="D:/课程资料/文本分析与挖掘"     # 含「第四章」「第五章」
export ZHIPUAI_API_KEY="你的 Key"                          # 仅智谱脚本需要
```

脚本会按 `TEXTMINING_DATA_DIR/第四章/深度学习评论.txt` 这类相对结构找数据。
`zhipu_scenic_comment_analysis.py` 原文件里曾有明文 API Key，已移除，必须用自己的 Key。
