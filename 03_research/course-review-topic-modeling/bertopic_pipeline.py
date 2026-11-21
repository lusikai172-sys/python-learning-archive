import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
import umap
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import KEYWORDS_XLSX, LABELED_XLSX, PREPROCESSED_XLSX  # noqa: E402

# 读取预处理后的 Excel 文件
file_path = PREPROCESSED_XLSX
df = pd.read_excel(file_path)

# 处理 NaN 值，将其替换为空字符串
df['final_text'] = df['final_text'].fillna('')

# 提取预处理后的文本数据
documents = df['final_text'].tolist()

# 1. 特征提取，使用 TfidfVectorizer
vectorizer = TfidfVectorizer()
embeddings = vectorizer.fit_transform(documents)

# 2. UMAP 降维
umap_model = umap.UMAP(
    n_neighbors=15,
    n_components=5,
    min_dist=0.01,
    metric='cosine'
)
umap_embeddings = umap_model.fit_transform(embeddings)

# 3. HDBSCAN 聚类（仅用于计算相似度和合并主题）
hdbscan_model_for_similarity = hdbscan.HDBSCAN(
    min_cluster_size=15,
    metric='euclidean',
    cluster_selection_method='eom'
)
labels = hdbscan_model_for_similarity.fit_predict(umap_embeddings)

# 计算每个主题的平均向量，用于衡量主题间的相似度
topic_vectors = []
for i in range(max(labels) + 1):
    if i != -1:  # 排除噪声点
        topic_indices = np.where(labels == i)[0]
        topic_embeddings = umap_embeddings[topic_indices]
        topic_vector = np.mean(topic_embeddings, axis=0)
        topic_vectors.append(topic_vector)

# 计算主题之间的相似度矩阵
similarity_matrix = cosine_similarity(topic_vectors)

# 设定一个相似度阈值，用于合并主题
similarity_threshold = 0.7
merged_labels = labels.copy()
for i in range(len(topic_vectors)):
    for j in range(i + 1, len(topic_vectors)):
        if similarity_matrix[i][j] > similarity_threshold:
            # 将相似度高的主题合并，这里简单地将第二个主题的标签改为第一个主题的标签
            indices_to_merge = np.where(labels == j)[0]
            merged_labels[indices_to_merge] = i

# 创建一个新的 HDBSCAN 模型实例供 BERTopic 使用
hdbscan_model_for_bertopic = hdbscan.HDBSCAN(
    min_cluster_size=15,
    metric='euclidean',
    cluster_selection_method='eom'
)

# 4. BERTopic 函数训练模型
topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=hdbscan_model_for_bertopic,
    calculate_probabilities=False,  # 设置为 False 避免计算概率
    min_topic_size=10,
    n_gram_range=(1, 2),
    top_n_words=10,
    low_memory=True
)

# 拟合模型并获取主题和概率
topics, _ = topic_model.fit_transform(documents, embeddings=umap_embeddings)

# 由于之前合并了主题，这里重新映射主题编号
new_topic_mapping = {}
new_topic_id = 0
# 确保包含所有可能的主题编号
all_possible_topics = set(topics).union(set(merged_labels))
for old_topic in all_possible_topics:
    if old_topic != -1:
        if old_topic not in new_topic_mapping:
            new_topic_mapping[old_topic] = new_topic_id
            new_topic_id += 1

new_topics = [new_topic_mapping.get(topic, -1) if topic != -1 else -1 for topic in topics]

# 准备将关键词输出到 Excel
keyword_data = []
for topic in set(new_topics):
    if topic != -1:
        top_words = topic_model.get_topic(topic)
        top_words = [word for word, _ in top_words]  # 提取关键词，忽略概率
        keyword_data.append({"主题": topic, "关键词": ", ".join(top_words)})

# 创建 DataFrame 并保存到 Excel
keyword_df = pd.DataFrame(keyword_data)
keyword_output_path = KEYWORDS_XLSX
keyword_output_path.parent.mkdir(parents=True, exist_ok=True)
keyword_df.to_excel(keyword_output_path, index=False)

# 保存带有主题标签的数据（可选）
df['topic'] = new_topics
output_file_path = LABELED_XLSX
df.to_excel(output_file_path, index=False)