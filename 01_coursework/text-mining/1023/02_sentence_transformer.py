import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from sentence_transformers import SentenceTransformer

# 假设我们有以下文档列表
with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]
# 加载模型
embedding_model = SentenceTransformer(str(BERT_MODEL_DIR))
# 调用SentenceTransformer工具直接拿到[CLS]对应的向量表示
embeddings = embedding_model.encode(texts, show_progress_bar=True)

print(embeddings.shape)
