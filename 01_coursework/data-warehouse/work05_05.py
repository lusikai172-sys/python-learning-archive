from sklearn.ensemble import IsolationForest
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

# 读取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 创建并配置孤立森林模型
clf = IsolationForest(contamination=0.03, random_state=42)
clf.fit(X)

# 获取样本的异常值得分以及预测的标签
scores = clf.decision_function(X)
labels = clf.predict(X)

# 绘制异常值检测结果的散点图
plt.figure(figsize=(5, 3))
# 绘制所有样本点，颜色根据原始类别标签
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='Set1')
# 单独绘制异常值点，用红色叉号标记
plt.scatter(X[labels == -1, 0], X[labels == -1, 1], marker='x', color='red', label='Outliers')
plt.legend()
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.title('Outlier Detection with Isolation Forest')
plt.show()

# 获取异常值的索引
outlier_indices = np.argwhere(labels == -1).T[0]

# 打印检测到的异常值和索引
print('检测到的异常值:')
for i, index in enumerate(outlier_indices):
    print(f"索引:{index},特征值:{X[index]}")