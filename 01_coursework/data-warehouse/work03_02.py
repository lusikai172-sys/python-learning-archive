import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, auc
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体，以便在图形中正确显示中文

# 1. 数据加载与预处理
df = pd.read_excel(DATA_DIR / "信用卡交易数据.xlsx")
features = ['换设备次数', '支付失败次数', '换IP次数', '换IP国次数', '交易金额']
target = '欺诈标签'

# 分离特征和目标变量
X = df[features]
y = df[target]

# 标准化处理
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 2. 构建分类模型
classifiers = {
    'RandomForest': RandomForestClassifier(),
    'AdaBoost': AdaBoostClassifier(),
    'XGBoost': XGBClassifier(),
    'LightGBM': LGBMClassifier()
}

for name, classifier in classifiers.items():
    # 模型训练
    classifier.fit(X_train, y_train)

    # 模型预测
    y_pred = classifier.predict(X_test)

    # 计算指标
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    print(f"{name}准确率: {acc:.4f}, 精确率: {prec:.4f}, 召回率: {rec:.4f}")

    # 绘制ROC曲线
    y_prob = classifier.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{name} (面积 = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')  # ROC曲线下的标准线
plt.xlabel('假阳性率')
plt.ylabel('真阳性率')
plt.title('ROC曲线')  # 将图片标题设置为中文
plt.legend(loc="lower right")
plt.show()

# 3. 使用GridSearchCV优化模型参数（以XGBoost为例）
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [100, 200, 300]
}
grid_search = GridSearchCV(XGBClassifier(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
print(f"XGBoost的最佳参数: {best_params}")

# 4. 特征重要性分析（以XGBoost为例）
xgb_model = XGBClassifier(**best_params)
xgb_model.fit(X_train, y_train)
feature_importances = xgb_model.feature_importances_
sorted_idx = np.argsort(feature_importances)[::-1]
pos = np.arange(sorted_idx.shape[0]) +.5
fig = plt.figure(figsize=(12, 6))
plt.barh(pos, feature_importances[sorted_idx], align='center')
plt.yticks(pos, np.array(features)[sorted_idx])
plt.xlabel('特征重要性')
plt.title('特征重要性排名')  # 将图片标题设置为中文
plt.show()