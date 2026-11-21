"""课程评论主题建模（BERTopic）的路径配置。

所有路径都可以用环境变量覆盖，未设置时回退到项目内相对目录，
避免脚本绑定某台机器上的绝对路径。

环境变量：
- COURSE_REVIEW_DATA_DIR   原始/中间数据目录，默认 ./data
- COURSE_REVIEW_OUTPUT_DIR 结果输出目录，默认 ./outputs
"""
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("COURSE_REVIEW_DATA_DIR", PROJECT_DIR / "data"))
OUTPUT_DIR = Path(os.environ.get("COURSE_REVIEW_OUTPUT_DIR", PROJECT_DIR / "outputs"))

# 输入：原始评论表（列为「评论」）
RAW_XLSX = DATA_DIR / "管理类课程评论.xlsx"
# 中间产物：分词 + 去停用词后的表（列为 final_text）
PREPROCESSED_XLSX = DATA_DIR / "管理类课程评论_预处理后.xlsx"
# 输出
KEYWORDS_XLSX = OUTPUT_DIR / "管理类课程评论_主题关键词.xlsx"
LABELED_XLSX = OUTPUT_DIR / "管理类课程评论_带主题标签.xlsx"

STOPWORDS_FILE = PROJECT_DIR / "stopwords.txt"
