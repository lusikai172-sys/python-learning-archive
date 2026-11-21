import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

# 示例代码：使用BERTopic进行主题建模
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import numpy as np

# 假设我们有以下文档列表
with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]

embedding_model = SentenceTransformer(str(BERT_MODEL_DIR))

# 用上一节的方法加载缓存的句子向量
save_path = f'{TEXT_DATA_DIR}/第五章/emb.npy'
embeddings = np.load(save_path)

# 初始化BERTopic模型
topic_model = BERTopic(embedding_model=embedding_model)
# 对文档进行主题建模
topics, probs = topic_model.fit_transform(texts, embeddings=embeddings)

# 继续使用上述的topic_model
topic_keywords = topic_model.get_topic_info()
topic_docs = topic_model.get_document_info(texts)

# 打印主题关键词
print(topic_keywords) # dataframe格式

# 保存结果
topic_keywords.to_excel(f'{TEXT_DATA_DIR}/第五章/测试bertopic.xlsx', sheet_name='Sheet1', index=False)
topic_docs.to_excel(f'{TEXT_DATA_DIR}/第五章/测试bertopic_doc.xlsx', sheet_name='Sheet1', index=False)


