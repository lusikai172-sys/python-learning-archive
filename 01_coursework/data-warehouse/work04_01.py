import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 生成聚类数据
data, _ = make_blobs(n_samples=1000, centers=4, random_state=0)

# 可视化数据
plt.scatter(data[:, 0], data[:, 1])
plt.show()

# 存储不同k值对应的SSE
sse = []
# 尝试的k值范围
k_values = range(2, 11)

# 计算不同k值下的SSE
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    sse.append(kmeans.inertia_)

# 绘制k值与SSE的相关性折线图
plt.plot(k_values, sse, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.title('Elbow Method to Determine Optimal k')
plt.show()

# 根据折线图确定2-3个备选k值，这里选取k=3, 4, 5作为备选
candidate_k_values = [3, 4, 5]

# 存储不同k值对应的轮廓系数
silhouette_scores = []

# 计算不同备选k值下的轮廓系数
for k in candidate_k_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    labels = kmeans.labels_
    silhouette_avg = silhouette_score(data, labels)
    silhouette_scores.append(silhouette_avg)

# 找到轮廓系数最高的k值对应的索引
best_index = np.argmax(silhouette_scores)
best_k = candidate_k_values[best_index]

print(f"表现最好的划分方案对应的k值为: {best_k}")