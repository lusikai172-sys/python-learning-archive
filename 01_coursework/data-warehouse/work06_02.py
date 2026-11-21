import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

# 设置中文字体为系统自带的黑体（Windows下示例，可根据实际调整）
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 1. 加载数据
housing = fetch_california_housing()
X = housing.data
y = housing.target
print(X[:5])  # 输出前5行特征数据
print(y[:5])  # 输出前5个目标值

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 数据预处理 - 标准化处理
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. 构建和训练模型
mlp = MLPRegressor(hidden_layer_sizes=(100, 50), activation='relu', learning_rate_init=0.001, max_iter=1000, random_state=42)
mlp.fit(X_train, y_train)

# 进行预测
y_pred = mlp.predict(X_test)

# 4. 模型评估
# 计算均方误差MSE
mse = mean_squared_error(y_test, y_pred)
print("均方误差MSE:", mse)

# 计算均方根误差RMSE
rmse = np.sqrt(mse)
print("均方根误差RMSE:", rmse)

# 真实值与预测值散点图
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("真实值")
plt.ylabel("预测值")
plt.title("真实值 vs 预测值")
plt.show()

# 5. 超参数调整 - 使用网格搜索GridSearchCV
param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (100, 50), (50, 30)],
    'activation': ['relu', 'tanh'],
    'learning_rate_init': [0.001, 0.01, 0.1]
}

grid_search = GridSearchCV(mlp, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

print("最佳超参数:", grid_search.best_params_)
print("最佳模型的均方误差:", -grid_search.best_score_)

# 使用最佳模型进行预测并绘制散点图
best_mlp = grid_search.best_estimator_
best_y_pred = best_mlp.predict(X_test)

# 重新计算均方误差MSE和均方根误差RMSE
best_mse = mean_squared_error(y_test, best_y_pred)
best_rmse = np.sqrt(best_mse)
print("最佳模型的均方根误差RMSE:", best_rmse)

# 真实值与预测值散点图（最佳模型）
plt.figure(figsize=(8, 6))
plt.scatter(y_test, best_y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("真实值")
plt.ylabel("预测值")
plt.title("最佳模型 - 真实值 vs 预测值")
plt.show()