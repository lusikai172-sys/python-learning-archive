import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

# 生成不同范围的一维数据
np.random.seed(42)
data = np.concatenate((
    np.random.normal(2, 0.6, 40),  # 均值为2，标准差为0.6，40个数据点
    np.random.normal(4, 0.4, 30),  # 均值为4，标准差为0.4，30个数据点
    np.random.normal(6, 0.5, 35)   # 均值为6，标准差为0.5，35个数据点
))

# 设置不同的簇个数
n_clusters = 3

# 设置不同的聚类策略
linkage_strategy = 'ward'

# 使用AgglomerativeClustering进行聚类
clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_strategy)
clusters = clustering.fit_predict(data.reshape(-1, 1))

# 可视化聚类结果
plt.figure(figsize=(10, 5))
for i in range(n_clusters):
    cluster_data = data[clusters == i]
    plt.scatter(np.arange(len(cluster_data)), cluster_data)
plt.title(f"Agglomerative Clustering Results with {linkage_strategy} Linkage and {n_clusters} Clusters")
plt.xlabel("Data Index")
plt.ylabel("Data Value")
plt.show()