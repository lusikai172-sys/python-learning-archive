import pandas as pd
# 读取csv文件中的数据
data=pd.read_csv('../data/data1.csv')
# data2=pd.read_excel('../data/2020-2022疫情数据.xlsx')
print(data,type(data))
# print(data.iloc[0:3,0:2])
# print(data2)
# 去除缺失数据 dropna()
data=data.dropna()
print(data)