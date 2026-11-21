import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

file_path = DATA_DIR / "客户价值数据表.xlsx"
data = pd.read_excel(file_path)
print(data.head())

target_variable_name = '客户价值'
feature_variables_names = ['历史贷款金额', '贷款次数', '学历', '月收入', '性别']

X = data[feature_variables_names]
y = data[target_variable_name]

# 计算相关系数矩阵（只取数值列，避免类别列导致 corr 报错）
correlation_matrix = data.select_dtypes(include="number").corr()

# 绘制相关性热力图
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 确保负号能正常显示

# 设置更大的图形尺寸以便更清晰展示
plt.figure(figsize=(12, 10))

# 选择更具视觉效果的配色方案，这里使用'YlGnBu'，你也可以尝试其他如'RdBu'、'GnBu'等
cmap = sns.cm.rocket_r
# cmap = sns.cm.RdBu
# cmap = sns.cm.GnBu

sns.heatmap(correlation_matrix, annot=True, cmap=cmap, fmt=".2f",
            linewidths=0.5, square=True, vmin=-1, vmax=1)

# 设置坐标轴字体为支持中文的字体
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)

plt.title('相关性热力图')
plt.show()

# 打印相关系数矩阵
print(correlation_matrix)

X = sm.add_constant(X)

# 创建并拟合模型
model = sm.OLS(y, X).fit()

# 打印回归报告
print(model.summary())