# 03_research · 论文与项目脚本

四个互不相关的分析任务，均为独立入口脚本，共享 `config.py` 做路径配置。

## course-review-topic-modeling — 课程评论主题建模

流程：Excel 语料 → jieba 分词 + 去停用词 → TF-IDF → UMAP + HDBSCAN → BERTopic 主题。

```bash
python preprocess_comments.py     # 产出 data/管理类课程评论_预处理后.xlsx
python bertopic_pipeline.py       # 产出 outputs/主题关键词.xlsx、带主题标签.xlsx
```

输入列：`评论`；中间结果列：`final_text`。
数据目录用 `COURSE_REVIEW_DATA_DIR` 指定，输出用 `COURSE_REVIEW_OUTPUT_DIR`。

## provincial-tourism-lda — 五省旅游政策文本 LDA

对安徽、广西、江西、山东、四川、浙江六份省级旅游政策文件（docx/pdf）做：

1. 文档解析与分句
2. jieba 分词（使用本地旅游领域词典）
3. LDA 主题建模，困惑度曲线选主题数
4. 主题雷达图、关键词共现网络、pyLDAvis 交互可视化

```bash
export LUO_SOURCE_DIR="D:/政策文件/细则"    # 存放 docx/pdf 的目录
python sichuan.py
```

产物写在脚本同目录（`*_topic_radar.png`、`*_cooccurrence_network.png`、
`*_lda_visualization.html`、`*_segmented_words.txt`），已随仓库保存。
`config.py` 中的默认路径是原作者桌面目录，换机器时请设 `LUO_SOURCE_DIR`。
六份政策原文未随代码归档，缺文件时脚本会提示读取失败并继续下一个。

## teaching-reform-analysis — 教改论文数据分析

`teacher_review_analysis.py`：评教明细 CSV → 清洗标准化 → 多模态融合模型
（数值特征 + one-hot + 文本，Dense + Attention 拼接）→ 保存 `fusion_model.h5`。

```bash
export TEACHING_DATA_DIR="D:/教改论文/数据整理"
python teacher_review_analysis.py
```

依赖 TensorFlow。评教数据含教师个人信息，**未归档、不建议公开**。

## misc-figures — 论文配图

| 文件 | 内容 |
|---|---|
| `fig_rfm_segments.py` | RFM 八类用户三维散点图（matplotlib 3D） |
| `rfm_3d_plot.html` | 同上，交互版（plotly 导出） |
| `fig_ui_optimization.py` | 页面加载耗时、任务步骤、满意度、转化漏斗四联图 |
| `preprocessed_rfm_data.xlsx` | RFM 绘图用的中间数据 |

纯绘图脚本，`python fig_rfm_segments.py` 直接出图，不依赖外部数据。
