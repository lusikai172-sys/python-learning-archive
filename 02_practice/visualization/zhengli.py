import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("VIS_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime
from numpy import poly1d
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")  # 忽略一些可能出现的警告信息，使输出更简洁

# 读取Excel文件中的地震数据
data_path = DATA_DIR / "中国地震数据（2012-2024）_ppman.xlsx"
df = pd.read_excel(data_path)

# 将发震时刻转换为相对天数（以数据中最早时间为基准），作为时间维度特征
df['发震时刻'] = pd.to_datetime(df['发震时刻'])
start_date = df['发震时刻'].min()
df['相对天数'] = (df['发震时刻'] - start_date).dt.days

# 提取特征，包含时间维度（相对天数）和空间维度（纬度、经度、深度）
features = df[['相对天数', '纬度(°)', '经度(°)', '深度(千米)']].values
# 目标变量为震级
target = df['震级(M)'].values

# 划分训练集和测试集，测试集占比30%
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# 创建XGBoost回归模型对象，可调整参数优化性能，如n_estimators（树的数量）、learning_rate（学习率）等
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# 训练模型
xgb_model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = xgb_model.predict(X_test)

# 计算均方误差来评估模型预测效果
mse = mean_squared_error(y_test, y_pred)
print("XGBoost模型的均方误差:", mse)

# 可视化部分，分析时间维度上震级的预测情况（使用seaborn和基础绘图功能实现）
# 创建一个新的图形，设置图形大小（单位：英寸）
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))

# 绘制真实震级随时间变化的折线图，添加线条样式、标记等细节
plt.plot(df.loc[X_test[:, 0].astype(int), '发震时刻'], y_test, label='真实震级', marker='o', markersize=5, linestyle='-', color='#1f77b4', linewidth=1.5)
# 绘制预测震级随时间变化的折线图，添加线条样式、标记等细节
plt.plot(df.loc[X_test[:, 0].astype(int), '发震时刻'], y_pred, label='预测震级', marker='s', markersize=5, linestyle='--', color='#ff7f0e', linewidth=1.5)

# 添加趋势线（简单示例，用多项式拟合来体现趋势，可根据实际情况调整拟合方式）
# 拟合真实震级的趋势线
z = np.polyfit(np.arange(len(y_test)), y_test, 3)
p = poly1d(z)
trendline_real = [p(i) for i in np.arange(len(y_test))]
plt.plot(df.loc[X_test[:, 0].astype(int), '发震时刻'], trendline_real, label='真实震级趋势线', linestyle=':', color='#1f77b4', linewidth=1.5)
# 拟合预测震级的趋势线
z_pred = np.polyfit(np.arange(len(y_pred)), y_pred, 3)
p_pred = poly1d(z_pred)
trendline_pred = [p_pred(i) for i in np.arange(len(y_pred))]
plt.plot(df.loc[X_test[:, 0].astype(int), '发震时刻'], trendline_pred, label='预测震级趋势线', linestyle=':', color='#ff7f0e', linewidth=1.5)

# 添加网格线，增强可读性，设置线型、颜色和透明度
plt.grid(True, linestyle='--', color='gray', alpha=0.5)

# 设置坐标轴标签、标题，并调整字体大小和样式
plt.xlabel('发震时刻', fontsize=14, fontweight='bold')
plt.ylabel('震级', fontsize=14, fontweight='bold')
plt.title('时间维度上真实震级与预测震级对比', fontsize=16, fontweight='bold')

# 设置坐标轴刻度标签的字体大小、旋转角度等样式，使其更美观易读
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)

# 设置图例的位置、字体大小和样式，使其更清晰
plt.legend(loc='upper left', fontsize=12, frameon=True, edgecolor='black')

# 调整图形的边距，让布局更合理
plt.tight_layout()

# 显示图形（注意，这里虽然底层用到了matplotlib，但没有直接使用其高级接口进行复杂操作）
plt.show()

# 可视化部分，分析空间维度上震级的预测情况（使用seaborn和基础绘图功能实现，以纬度为例，可拓展到经度等）
# 绘制真实震级与纬度关系的散点图，设置更多样式细节
sns.scatterplot(data=df, x='纬度(°)', y='震级(M)', label='真实震级', color='blue', alpha=0.6, s=50, edgecolor='black', linewidth=0.5)

# 拟合真实震级与纬度关系的曲线（简单示例，用多项式拟合，可调整拟合方式）
z_lat = np.polyfit(df['纬度(°)'].values, target, 3)
p_lat = poly1d(z_lat)
lat_fit_data = {'纬度(°)': df['纬度(°)'].values, '震级': p_lat(df['纬度(°)'].values)}
plt.plot(lat_fit_data['纬度(°)'], lat_fit_data['震级'], label='真实震级拟合曲线（纬度）', linestyle=':', color='blue', linewidth=1.5)

# 拟合预测震级与纬度关系的曲线
z_lat_pred = np.polyfit(df['纬度(°)'].values, xgb_model.predict(features), 3)
p_lat_pred = poly1d(z_lat_pred)
lat_fit_data_pred = {'纬度(°)': df['纬度(°)'].values, '震级': p_lat_pred(df['纬度(°)'].values)}
plt.plot(lat_fit_data_pred['纬度(°)'], lat_fit_data_pred['震级'], label='预测震级拟合曲线（纬度）', linestyle=':', color='red', linewidth=1.5)

# 分箱统计并绘制不同纬度区间内真实震级和预测震级的均值箱线图（展示数据分布情况）
bin_size = 5
bins = np.arange(int(df['纬度(°)'].min()), int(df['纬度(°)'].max()) + bin_size, bin_size)
df['纬度区间'] = pd.cut(df['纬度(°)'], bins=bins)
grouped_real = df.groupby('纬度区间')['震级(M)'].mean()
grouped_pred = df.groupby('纬度区间')[['纬度(°)', xgb_model.predict(features)]].mean()
grouped_pred = grouped_pred.rename(columns={xgb_model.predict(features).name: '预测震级均值'})

box_data = pd.concat([grouped_real.reset_index(), grouped_pred.reset_index()], axis=1).melt(id_vars='纬度区间')
sns.boxplot(data=box_data, x='纬度区间', y='value', hue='variable', palette='Set2')
plt.xlabel('纬度区间', fontsize=14, fontweight='bold')
plt.ylabel('震级均值', fontsize=14, fontweight='bold')
plt.title('不同纬度区间内真实震级与预测震级均值分布对比', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc='upper right', fontsize=12, frameon=True, edgecolor='black')

# 调整图形的边距，让布局更合理
plt.tight_layout()

# 显示图形
plt.show()