import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV


# 自定义函数用于绘制混淆矩阵
def plot_confusion_matrix_custom(cm, classes,
                                 normalize=False,
                                 title='Confusion matrix',
                                 cmap=plt.cm.Blues):
    """
    绘制混淆矩阵的函数
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("归一化混淆矩阵")
    else:
        print('未归一化混淆矩阵')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap, vmin=0, vmax=1 if normalize else cm.max())
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# 1. 加载数据
wine = load_wine()
X = wine.data
y = wine.target
print("数据集前5行数据：")
print(X[:5])
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. 数据预处理 - 标准化处理
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. 构建和训练模型
mlp = MLPClassifier(hidden_layer_sizes=(100,), activation='relu', learning_rate_init=0.01, max_iter=1000, random_state=42)
mlp.fit(X_train, y_train)

# 4. 模型评估
y_pred = mlp.predict(X_test)
print("分类报告：")
print(classification_report(y_test, y_pred))

print("混淆矩阵：")
print(confusion_matrix(y_test, y_pred))

# 可视化混淆矩阵，调用自定义的绘制函数
confusion_mtx = confusion_matrix(y_test, y_pred)
class_names = wine.target_names
# 设置图形大小
plt.figure(figsize=(8, 6))
plot_confusion_matrix_custom(confusion_mtx, classes=class_names,
                             title='Confusion matrix for Wine Classification')
plt.show()

# 5. 超参数调整
param_grid = {
    'hidden_layer_sizes': [(20,), (50,), (20, 10)],
    'activation': ['tanh', 'relu'],
    'learning_rate_init': [0.001, 0.01, 0.1]
}
grid_search = GridSearchCV(MLPClassifier(max_iter=1000, random_state=42), param_grid, cv=3)
grid_search.fit(X_train, y_train)
print("最佳参数：", grid_search.best_params_)
print("最佳交叉验证得分：", grid_search.best_score_)