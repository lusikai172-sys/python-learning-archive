import pandas as pd
df=pd.read_csv('../data/data8.csv',sep='|')
print(df)
df['result']=df.price*df.num
print(df)
'''
    df.mean()   返回所有列的均值
    mean(1)  返回所有行的均值   下同
    corr() 返回列与列之间的相关系数
    count()  返回每一列中的非空值的个数
    max()  每一列的最大值
    min()   每一列的最小值
    median()  每一列的中位数
    std()  每一列的标准差
    var()   方差
    mode()   众数
'''