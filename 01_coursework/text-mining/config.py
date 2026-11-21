"""文本挖掘课程练习的路径配置。

优先读环境变量，未配置时回退到原作者本机路径，便于在新机器上迁移。

环境变量：
- BERT_MODEL_DIR        本地 bert-base-chinese 模型目录
- TEXTMINING_DATA_DIR   课程数据根目录（其下应有「第四章」「第五章」）
- TEXTMINING_OUTPUT_DIR 输出目录，默认 ./outputs
"""
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
BERT_MODEL_DIR = Path(os.environ.get("BERT_MODEL_DIR", r"D:/bert-base-chinese"))
TEXT_DATA_DIR = Path(
    os.environ.get(
        "TEXTMINING_DATA_DIR",
        r"D:/成都理工大学重要文件夹/课程《文本分析与挖掘》相关/数据/2024-2025（一）",
    )
)
OUTPUT_DIR = Path(os.environ.get("TEXTMINING_OUTPUT_DIR", PROJECT_DIR / "outputs"))
STOPWORDS_FILE = PROJECT_DIR / "停用词.txt"
