import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score  # 添加这行导入语句


# 计算Hopkins统计量
def hopkins(data):
    n = len(data)
    d = data.shape[1]

    m = int(0.1 * n)  # 选择10%的数据点作为随机样本

    rng = np.random.RandomState(42)
    rand_indices = rng.randint(0, n, m)
    x = data[rand_indices]

    neigh = NearestNeighbors(n_neighbors=1).fit(data)
    u_distances, _ = neigh.kneighbors(x, return_distance=True)

    w = np.random.uniform(0, 1, size=(m, d))
    w_distances, _ = neigh.kneighbors(w, return_distance=True)

    h = np.sum(u_distances) / (np.sum(u_distances) + np.sum(w_distances))

    return h


# 使用DBSCAN算法进行聚类并绘图
def dbscan_cluster_and_plot():
    # 生成月亮数据集，降低噪声水平并增加样本数量
    data, _ = make_moons(n_samples=1000, noise=0.05, random_state=42)

    # 数据预处理：标准化
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # 计算Hopkins统计量估计聚类趋势
    hopkins_stat = hopkins(data_scaled)
    print("Hopkins统计量:", hopkins_stat)

    # 尝试不同的DBSCAN参数组合
    eps_values = [0.2, 0.25, 0.3]
    min_samples_values = [3, 4, 5]

    best_labels = None
    best_silhouette_score = -1

    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            dbscan.fit(data_scaled)
            labels = dbscan.labels_

            # 计算轮廓系数来评估聚类效果
            silhouette_score_value = silhouette_score(data_scaled, labels)

            if silhouette_score_value > best_silhouette_score:
                best_silhouette_score = silhouette_score_value
                best_labels = labels

    # 绘制聚类结果
    plt.scatter(data_scaled[best_labels == 0][:, 0], data_scaled[best_labels == 0][:, 1], c="red", marker='o',
                label='class0')
    plt.scatter(data_scaled[best_labels == 1][:, 0], data_scaled[best_labels == 1][:, 1], c="blue", marker='*',
                label='class1')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    dbscan_cluster_and_plot()