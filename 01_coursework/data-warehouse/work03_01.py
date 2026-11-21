import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
from sklearn.preprocessing import OneHotEncoder

# 设置中文字体为黑体（SimHei），解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 读取信用卡精准营销数据
data_path = DATA_DIR / "信用卡精准营销模型.xlsx"
df = pd.read_excel(data_path)

# 对性别列进行独热编码
encoder = OneHotEncoder()
gender_encoded = encoder.fit_transform(df[['性别']])
gender_encoded_df = pd.DataFrame(gender_encoded.toarray(), columns=encoder.get_feature_names_out(['性别']))
df = pd.concat([df.drop('性别', axis=1), gender_encoded_df], axis=1)

# 划分特征和目标变量
X = df.drop('响应', axis=1)
y = df['响应']

# 将数据集划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 决策树分类模型
def decision_tree_model():
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("决策树模型：")
    print("准确率：", accuracy)
    print("精确度：", precision)
    print("召回率：", recall)
    print("F1值：", f1)

    # 计算ROC曲线和AUC值
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label='决策树 (AUC = %0.2f)' % roc_auc)
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('ROC曲线 - 决策树')
    plt.legend(loc="lower right")
    plt.show()

    return accuracy, precision, recall, f1, roc_auc


# 支持向量机分类模型
def svm_model():
    classifier = svm.SVC(kernel='linear', probability=True)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("支持向量机模型：")
    print("准确率：", accuracy)
    print("精确度：", precision)
    print("召回率：", recall)
    print("F1值：", f1)

    # 计算ROC曲线和AUC值
    y_pred_proba = classifier.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label='支持向量机 (AUC = %0.2f)' % roc_auc)
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('ROC曲线 - 支持向量机')
    plt.legend(loc="lower right")
    plt.show()

    return accuracy, precision, recall, f1, roc_auc


# 最近邻分类模型（以KNN为例，K取5）
def knn_model():
    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("最近邻模型（KNN）：")
    print("准确率：", accuracy)
    print("精确度：", precision)
    print("召回率：", recall)
    print("F1值：", f1)

    # 计算ROC曲线和AUC值
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label='KNN (AUC = %0.2f)' % roc_auc)
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('ROC曲线 - KNN')
    plt.legend(loc="lower right")
    plt.show()

    return accuracy, precision, recall, f1, roc_auc


# 朴素贝叶斯分类模型
def naive_bayes_model():
    clf = GaussianNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("朴素贝叶斯模型：")
    print("准确率：", accuracy)
    print("精确度：", precision)
    print("召回率：", recall)
    print("F1值：", f1)

    # 计算ROC曲线和AUC值
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label='朴素贝叶斯 (AUC = %0.2f)' % roc_auc)
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('ROC曲线 - 朴素贝叶斯')
    plt.legend(loc="lower right")
    plt.show()

    return accuracy, precision, recall, f1, roc_auc


if __name__ == "__main__":
    dt_results = decision_tree_model()
    svm_results = svm_model()
    knn_results = knn_model()
    nb_results = naive_bayes_model()

    # 比较各模型的AUC值，选择表现最好的模型
    models = ['决策树', '支持向量机', '最近邻（KNN）', '朴素贝叶斯']
    auc_values = [dt_results[4], svm_results[4], knn_results[4], nb_results[4]]
    best_model_index = np.argmax(auc_values)
    best_model = models[best_model_index]

    print("综合表现最好的模型是：", best_model)