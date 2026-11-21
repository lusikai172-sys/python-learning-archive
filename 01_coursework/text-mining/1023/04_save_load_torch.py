import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

# 假设我们有以下文档列表
with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]

from transformers.pipelines import pipeline
embedding_model = pipeline(
    task='feature-extraction',
    model=str(BERT_MODEL_DIR)
)
output = embedding_model(texts) # 注意，这里的output格式为list
import torch
# 第一步：获取每个句子的向量表示，并转化为list[torch.tensor]格式
sentence_embeddings = [torch.tensor(i[0][0], dtype=torch.float32) for i in output]
# 第二步：合并
output_all = torch.stack(sentence_embeddings)

# 保存
save_path = '位置/emb.pt'
torch.save(output_all, save_path)
# 加载
sentence_embeddings = torch.load(save_path)