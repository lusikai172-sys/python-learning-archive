import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import statsmodels.api as sm

# 指定默认字体，解决中文显示及负号显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读取Excel文件中的数据
file_path = DATA_DIR / "行业收入表-餐饮服务.xlsx"
data = pd.read_excel(file_path)

# 提取工龄和薪水列
X = data[['工龄']].values
Y = data['薪水'].values

# 一、绘制工龄和薪水之间关系的散点图
plt.scatter(X, Y, color='orange', label='数据点')
plt.xlabel('工龄')
plt.ylabel('薪水')
plt.title('餐饮服务业工龄与薪水的关系')
plt.legend()
plt.grid(True)
plt.show()

# 二、搭建一元线性回归模型进行分析
# 训练线性回归模型
regr = LinearRegression()
regr.fit(X, Y)

# 打印回归模型的系数和截距
print('系数a（工龄的系数）为:', regr.coef_[0])
print('截距b为:', regr.intercept_)

# 利用statsmodels包得到回归报告
X_with_constant = sm.add_constant(X)  # 添加常数项，对应截距，符合statsmodels格式要求
model_statsmodels = sm.OLS(Y, X_with_constant).fit()  # 构建并拟合普通最小二乘法（OLS）回归模型
print(model_statsmodels.summary())  # 输出回归报告，包含众多统计信息如系数的显著性等

# 划分训练集和测试集（这里按8:2划分）
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 利用训练好的模型对测试集进行预测
Y_pred_linear = regr.predict(X_test)

# 利用sklearn.metrics计算R2、MAE、MSE等模型评价指标
r2_linear = r2_score(Y_test, Y_pred_linear)
mae_linear = mean_absolute_error(Y_test, Y_pred_linear)
mse_linear = mean_squared_error(Y_test, Y_pred_linear)
print(f"一元线性回归模型的R2值为: {r2_linear:.2f}")
print(f"一元线性回归模型的MAE值为: {mae_linear:.2f}")
print(f"一元线性回归模型的MSE值为: {mse_linear:.2f}")

# 三、搭建多项式回归模型进行分析，尝试3个不同的最高次项（2、3、4）
degrees = [2, 3, 4]
r2_poly_list = []  # 用于存储多项式回归模型的R2值
for degree in degrees:
    # 生成多项式特征
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X_train)

    # 训练多项式回归模型
    model_poly = LinearRegression().fit(X_poly, Y_train)

    # 在测试集上进行预测（需要先对测试集也转换为对应的多项式特征形式）
    X_test_poly = poly_features.transform(X_test)
    Y_pred_poly = model_poly.predict(X_test_poly)

    # 计算相应的评价指标（以R2为例，也可同时考虑MAE、MSE等）
    r2_poly = r2_score(Y_test, Y_pred_poly)
    r2_poly_list.append(r2_poly)  # 将本次多项式回归的R2值添加到列表中
    mae_poly = mean_absolute_error(Y_test, Y_pred_poly)
    mse_poly = mean_squared_error(Y_test, Y_pred_poly)
    print(f"最高次项为{degree}的多项式回归模型的R2值为: {r2_poly:.2f}")
    print(f"最高次项为{degree}的多项式回归模型的MAE值为: {mae_poly:.2f}")
    print(f"最高次项为{degree}的多项式回归模型的MSE值为: {mse_poly:.2f}")

    # 可根据实际情况进行可视化展示（这里暂省略具体可视化代码，可绘制多项式回归的拟合曲线等）

# 四、综合进行最佳模型选择（以R2值为例）
best_model = None
best_r2 = -np.inf
models_info = {
    "一元线性回归": (r2_linear, mae_linear, mse_linear),
    f"多项式回归（最高次项为2）": (r2_poly_list[0] if len(r2_poly_list) > 0 else None, None, None),
    f"多项式回归（最高次项为3）": (r2_poly_list[1] if len(r2_poly_list) > 1 else None, None, None),
    f"多项式回归（最高次项为4）": (r2_poly_list[2] if len(r2_poly_list) > 2 else None, None, None),
}

for model_name, (r2, _, _) in models_info.items():
    if r2 is not None and r2 > best_r2:  # 增加判断r2是否为None，只有不为None时才进行比较
        best_r2 = r2
        best_model = model_name

print(f"综合比较后，最佳模型为：{best_model}")