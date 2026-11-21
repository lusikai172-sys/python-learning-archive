import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#读取文件
df = pd.DataFrame(pd.read_csv('../classwork_02_weibo_hotsearch/微博热搜处理后.csv'))
#输出信息
print(df)


# #进行数据分析与可视化
# X = df.drop("热度", axis = 1)
# predict_model = LinearRegression()
# predict_model.fit(X, df['排名'])    #训练模型
# print("回归系数为：", predict_model.coef_)   # 判断相关性



#绘制散点图
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import numpy as np
# %matplotlib inline  # Jupyter 专用魔法命令，在 .py 脚本中无效，已注释
排名 = (df["排名"])
热度 = (df["热度"])
plt.rcParams['font.sans-serif']=['SimHei'] #用于正常显示中文标签
plt.figure(figsize=(8,5))
plt.scatter(排名,热度,color=[0,0,1,0.4],label=u"样本数据",linewidth=2)  #颜色用RGB值
plt.title("排名 scatter",color="blue")
plt.xlabel("排名")
plt.ylabel("热度")
plt.legend()
plt.grid()
plt.show()
#
#
# #回归散点图
# import seaborn as sns
# sns.regplot(df.排名,df.热度)
# plt.title('排名热度回归散点图')
#
#
# #绘制柱状图
# plt.figure()
# x=np.arange(0,20)
# y=df.loc['1':'20','热度']  #选取画图数据范围
# plt.bar(x, y,color='c',alpha=0.5) #增加透明度 使图更加美观
# plt.xlabel('排名')
# plt.ylabel('热度')
# plt.title("热搜数据")
# plt.show()
#
#
# # 绘制折线图
# plt.figure()
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# x=np.arange(0,20)
# y=df.loc['1':'20','热度']  #选取画图数据范围
# plt.plot(x, y,'r-o',color='blue')
# plt.xlabel('排名')
# plt.ylabel('热度')
# plt.title("热搜数据")
# plt.show()
#
#
# #绘制盒图
# def box():
#     plt.title('热度与排名盒图')
#     sns.boxplot(x='排名',y='热度', data=df)
# box()
#
#
# #用Seaborn绘制各种分布图
# sns.jointplot(x="排名",y='热度',data = df, kind='kde', color='r')
# sns.jointplot(x="排名",y='热度',data = df, kind='hex')
# sns.distplot(df['热度'])
#
#
# # 绘制单核密度图
# sns.kdeplot(df['热度'])
#
#
# #绘制排名与热度的回归图
# sns.regplot(df.排名,df.热度)
#
#
# # 用最小二乘法得出一元二次拟合方程
# plt.figure(figsize=(13,6))
# plt.scatter(排名,热度,color=[0,0,0.8,0.4],label=u"样本数据",linewidth=2)
# plt.xlabel("排名")
# plt.ylabel("热度")
# plt.legend()
# def func(p,x):
#     a,b,c=p
#     return a*(x**2)+(b*x)+c
# def er_func(p,x,y):
#     return func(p,x)-y
# p0=[2,3,4]
# P=leastsq(er_func,p0,args=(排名,热度))
# a,b,c=P[0]
# x=np.linspace(0,55,100)
# y=a*(x**2)+(b*x)+c
# plt.plot(x,y,color=[0,0,0.8,0.4],label=u"拟合直线",linewidth=2)
# plt.scatter(x,y,color="c",label=u"样本数据",linewidth=2)
# plt.legend()
# plt.title('排名热度回归曲线')
# plt.grid()
# plt.show()
