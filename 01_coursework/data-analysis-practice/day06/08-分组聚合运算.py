import pandas as pd
# 读取数据
df=pd.read_csv('../data/groupby.csv')
print(df)
# 各地区的人数  count
res1=df.groupby('address')['id'].count().reset_index()
print(res1)
res1=df.groupby('address')['score'].mean().reset_index()
res1=df.groupby('address')['score'].sum().reset_index()
print(res1)
# agg  聚合
res2=df.groupby('address')['score'].agg(['max','min','mean']).reset_index()
print(res2)
res3=df.groupby('address').agg({'score':'min','age':'max'}).reset_index()
print(res3)
# 排序
print(df.sort_values(by='age',ascending=True))
# 获取某列出现频率
print(df.score.value_counts)