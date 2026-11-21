# 数据目录

默认从本目录读取，可用 `COURSE_REVIEW_DATA_DIR` 覆盖。

| 文件 | 用途 | 必需列 |
|---|---|---|
| `管理类课程评论.xlsx` | 原始语料（输入） | `评论` |
| `管理类课程评论_预处理后.xlsx` | 分词去停用词后的中间结果 | `final_text` |

`preprocess_comments.py` 读取前者并生成后者；`bertopic_pipeline.py` 读取后者，
把关键词表与带主题标签的表写到 `../outputs/`。

语料为课程评论文本，未随代码归档；如需复现请自备同结构 Excel。
