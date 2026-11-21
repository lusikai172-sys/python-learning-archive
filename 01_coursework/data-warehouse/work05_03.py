from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

# 读取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data

# 设置新的DBSCAN算法参数并拟合数据
# 调整eps和min_samples的值
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan.fit(X)

# 获取异常值的布尔数组及对应索引
outliers_mask = dbscan.labels_ == -1
outliers_indices = np.where(outliers_mask)[0]

# 获取每个样本所属的簇标签
cluster_labels = dbscan.labels_

# 绘制异常值检测结果图
plt.figure(figsize=(5, 3))

# 绘制正常样本
plt.scatter(X[~outliers_mask, 0], X[~outliers_mask, 1],
            c=cluster_labels[~outliers_mask], cmap='viridis', label='Normal')

# 绘制异常值
plt.scatter(X[outliers_mask, 0], X[outliers_mask, 1], c='red', label='Outlier')

plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('DBSCAN Outlier Detection on Iris Dataset')
plt.legend()
plt.show()

# 显示检测出的异常值和索引
print('检测到的异常值:')
for i, index in enumerate(outliers_indices):
    print(f"索引:{index},特征值:{X[index]}")