from sklearn.neighbors import LocalOutlierFactor
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

# 读取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data

# 设置LocalOutlierFactor模型参数并拟合数据
model = LocalOutlierFactor(n_neighbors=5, novelty=True, contamination=0.05)
model.fit(X)

# 预测样本点是否为异常值，正常返回1，异常返回-1
y_pred = model._predict(X)

# 绘制散点图展示样本点及异常值情况
plt.figure(figsize=(5, 3))
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('LOF Outlier Detection on Iris Dataset')
plt.show()

# 获取异常值的索引
outliers_indices = np.argwhere(y_pred == -1).T[0]

# 打印检测到的异常值和索引
print('检测到的异常值:')
for i, index in enumerate(outliers_indices):
    print(f"索引:{index},特征值:{X[index]}")