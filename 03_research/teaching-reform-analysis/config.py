"""教改论文（教师评教数据）分析的路径配置。

环境变量：
- TEACHING_DATA_DIR  评教明细 CSV 所在目录，默认 ./data
- TEACHING_OUTPUT_DIR 模型与图表输出目录，默认 ./outputs
"""
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("TEACHING_DATA_DIR", PROJECT_DIR / "data"))
OUTPUT_DIR = Path(os.environ.get("TEACHING_OUTPUT_DIR", PROJECT_DIR / "outputs"))

RAW_CSV = DATA_DIR / "2021-2022-2评教统计明细.csv"
MODEL_H5 = OUTPUT_DIR / "fusion_model.h5"
