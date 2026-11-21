import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
import seaborn as sns

# 读取鸢尾花数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 创建DataFrame
iris_df = pd.DataFrame(X, columns=iris.feature_names[:4])

# 设置绘图风格
sns.set_style("whitegrid")

# 绘制箱线图
plt.figure(figsize=(7, 3))
ax = sns.boxplot(data=iris_df)
plt.title('Boxplot of Iris Dataset Features')
plt.xlabel('Features')
plt.ylabel('Values')
plt.show()

# 检测离群点
outliers = []
for feature in iris_df.columns:
    q1 = iris_df[feature].quantile(0.25)
    q3 = iris_df[feature].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    feature_outliers = iris_df[(iris_df[feature] < lower_bound) | (iris_df[feature] > upper_bound)]
    outliers.extend(feature_outliers.index)

# 去除重复的异常值索引
outliers = list(set(outliers))
outliers.sort()

# 打印检测出的异常值和索引
print('检测出的离群点:')
for index in outliers:
    print(f"Index: {index}, Values: {iris_df.loc[index].values}")