import os
from pathlib import Path

from executing import Source
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier,export_graphviz
import pydotplus
from PIL import Image as PILImage
import io

def knn_iris():
    '''
    用KNN算法对鸢尾花进行分类
    :return:
    '''
    #1）获取数据
    iris = load_iris()
    #2）划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=32)
    #3）特征工程：标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    #4)KNN算法预估器
    estimator = KNeighborsClassifier(n_neighbors=3)   #n_neighbors即为k值
    estimator.fit(x_train,y_train)
    #5）模型评估
    #方法一：直接比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("直接比对真实值和预测值:\n",y_test == y_predict)

    #方法二：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    return None



def knn_iris_gscv():
    '''
    用KNN算法对鸢尾花进行分类，添加网格搜索和交叉验证
    :return:
    '''
    #1）获取数据
    iris = load_iris()
    #2）划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=32)
    #3）特征工程：标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    #4)KNN算法预估器
    estimator = KNeighborsClassifier(n_neighbors=3)   #n_neighbors即为k值

    #加入网格搜索和交叉验证
    #参数准备
    param_dict = {"n_neighbors":[1,3,5,7,9,11]}
    estimator = GridSearchCV(estimator,param_grid=param_dict,cv=10)
    estimator.fit(x_train,y_train)
    #5）模型评估
    #方法一：直接比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("直接比对真实值和预测值:\n",y_test == y_predict)

    #方法二：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    print("最佳参数：\n",estimator.best_params_)
    print("最佳结果：\n", estimator.best_score_)
    print("最佳估计器：\n", estimator.best_estimator_)
    print("交叉验证结果：\n", estimator.cv_results_)

    return None


def nb_news():
    '''
    用朴素贝叶斯算法对新闻进行分类
    :return:
    '''
    #1)获取数据
    news = fetch_20newsgroups(data_home=os.environ.get("SKLEARN_DATA_HOME", str(Path(__file__).resolve().parent / "sklearn_datasets")),subset="all")
    #2)划分数据集
    x_train,x_test,y_train,y_test =  train_test_split(news.data,news.target,random_state=33)
    #3)特征工程：文本特征抽取——tfidf
    transfer = TfidfVectorizer()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    #4)朴素贝叶斯预估器流程
    estimator = MultinomialNB()
    estimator.fit(x_train,y_train)

    #5)模型评估
    #方法一：直接比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("直接比对真实值和预测值:\n",y_test == y_predict)

    #方法二：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    return None


def decision_iris():
    '''
    用决策树对鸢尾花进行分类
    :return:
    '''
    #1)划分数据集
    iris = load_iris()
    #2)划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=33)
    #3)决策树预估器
    estimator = DecisionTreeClassifier(criterion="entropy")
    estimator.fit(x_train,y_train)
    #4)模型评估
    #方法一：直接比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("直接比对真实值和预测值:\n",y_test == y_predict)

    #方法二：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    # 可视化决策树（不保存文件，直接显示）
    dot_data = export_graphviz(
        estimator,
        feature_names=iris.feature_names,
        class_names=iris.target_names,
        rounded=True,
        filled=True,
        out_file=None  # 设置为None不生成文件，直接返回dot数据
    )

    # 使用pydotplus转换dot数据为图形
    graph = pydotplus.graph_from_dot_data(dot_data)
    img_data = graph.create_png()

    # 将二进制数据转换为PIL图像并显示
    img = PILImage.open(io.BytesIO(img_data))
    img.show()  # 在PyCharm中弹出窗口显示图像

    return None



if __name__ == "__main__":
    #代码1：用KNN算法对鸢尾花进行分类
    #knn_iris()
    #代码2：用KNN算法对鸢尾花进行分类，添加网格搜索和交叉验证
    #knn_iris_gscv()
    #代码3：用朴素贝叶斯算法对新闻进行分类
    #nb_news()
    #代码4：用决策树对鸢尾花进行分类
    decision_iris()
