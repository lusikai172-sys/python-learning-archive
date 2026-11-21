from sklearn import datasets
import numpy as np

# 读取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 定义要修改的数据点索引及对应的修改后的值
modifications = {
    10: [7, 3.9, 5, 0.2],
    20: [6, 5, 4, 1.5],
    30: [5, 5, 3, 0.2],
    60: [5, 2, 3.5, 3],
    80: [5.5, 6, 3.8, 1.1]
}

# 手动修改数据以产生偏差
for index, new_values in modifications.items():
    X[index] = new_values

print('修改后的数据最大值:', np.max(X, axis=0))
print('修改后的数据最小值:', np.min(X, axis=0))