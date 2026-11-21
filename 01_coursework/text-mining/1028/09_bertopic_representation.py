import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

# 示例代码：使用BERTopic进行话题建模
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

import numpy as np


# 假设我们有以下文档列表
with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]

stopwords_file = f'{TEXT_DATA_DIR}/第二章/停用词.txt'
with open(stopwords_file, 'r') as f:
    stopword_list = [word.strip() for word in f.readlines()]

embedding_model = SentenceTransformer(str(BERT_MODEL_DIR))
save_path = f'{TEXT_DATA_DIR}/第五章/emb.npy'

# 调用SentenceTransformer工具对文本进行句子级向量化
embeddings = np.load(save_path)

# 定义降维方法
from umap import UMAP
# umap_model = UMAP(n_components=2, metric='cosine')
umap_model = UMAP(n_components=2, metric='cosine', random_state=42)
# n_components表示降维后的维度。

# 定义聚类方法
from hdbscan import HDBSCAN
hdbscan_model = HDBSCAN(min_cluster_size=2, prediction_data=True)
# min_cluster_size表示每个簇中最少的样本数量

# 定义分词工具
from sklearn.feature_extraction.text import CountVectorizer
import jieba
def tokenize_zh(text):
    words = jieba.lcut(text)
    return words
vectorizer_model = CountVectorizer(tokenizer=tokenize_zh, stop_words=stopword_list)

# 定义关键词提取工具
from bertopic.vectorizers import ClassTfidfTransformer
ctfidf_model = ClassTfidfTransformer()

# # 初始化BERTopic模型
# topic_model = BERTopic(
#     embedding_model=embedding_model,
#     umap_model=umap_model,
#     hdbscan_model=hdbscan_model,
#     vectorizer_model=vectorizer_model,
#     ctfidf_model=ctfidf_model,
#     calculate_probabilities=True,
#     top_n_words=5
# )

from bertopic.representation import MaximalMarginalRelevance
representation_model = MaximalMarginalRelevance(diversity=0.3)
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    calculate_probabilities=True,
    top_n_words=5,
    representation_model=representation_model
)
# 对文档进行话题建模
topics, probs = topic_model.fit_transform(texts, embeddings=embeddings)
# 继续使用上述的topic_model
topic_keywords = topic_model.get_topic_info()
topic_docs = topic_model.get_document_info(texts)
# 打印话题关键词
print(topic_keywords) # dataframe格式
topic_keywords.to_excel(f'{TEXT_DATA_DIR}/第五章/bertopic优化主题表示.xlsx', sheet_name='Sheet1', index=False)
topic_docs.to_excel(f'{TEXT_DATA_DIR}/第五章/bertopic优化主题表示_doc.xlsx', sheet_name='Sheet1', index=False)

print(topics[:10])
print(probs[:10])
