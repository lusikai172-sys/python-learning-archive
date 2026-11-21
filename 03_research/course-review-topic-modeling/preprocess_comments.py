import pandas as pd
import re
import jieba
from config import PREPROCESSED_XLSX, RAW_XLSX, STOPWORDS_FILE  # noqa: E402

# 读取 Excel 文件
file_path = RAW_XLSX
df = pd.read_excel(file_path)

# 步骤 1: 标记化和排除特殊字符
def tokenize_and_remove_special(text):
    # 处理缺失值
    if pd.isna(text):
        text = ''
    # 排除特殊字符和标点符号，仅保留中文和英文字符
    text = re.sub(r'[^a-zA-Z\u4e00-\u9fa5\s]', '', text)
    # 进行中文分词
    tokens = jieba.lcut(text)
    return ' '.join(tokens)

df['processed_text'] = df['评论'].apply(tokenize_and_remove_special)

# 步骤 2: 读取停用词并去除
def read_stopwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = [line.strip() for line in f.readlines()]
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='gbk') as f:
            stopwords = [line.strip() for line in f.readlines()]
    return set(stopwords)

# 停用词文件路径
stopwords_path = STOPWORDS_FILE
stop_words = read_stopwords(stopwords_path)

def remove_stopwords(text):
    words = text.split()
    return ' '.join([word for word in words if word not in stop_words])

df['final_text'] = df['processed_text'].apply(remove_stopwords)

# 保存预处理后的数据到新的 Excel 文件（可选）
output_file_path = PREPROCESSED_XLSX
output_file_path.parent.mkdir(parents=True, exist_ok=True)
df.to_excel(output_file_path, index=False)