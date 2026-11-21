import pandas as pd
# df1=pd.read_csv('../data/data6-1.csv',sep='|')
# df2=pd.read_csv('../data/data6-2.csv',sep='|')
# df3=pd.read_csv('../data/data6-3.csv',sep='|')
#
# new_Df=pd.concat([df1,df2,df3]).reset_index(drop=False)
# # reset_index   重置索引
# # drop=True  原来的索引删掉然后重置
# # drop=False  保留原来的索引作为新的一列index,重新添加索引
# print(new_Df)
df1=pd.read_csv('../data/data7-1.csv',sep='|',names=['id','comments','title'])
df2=pd.read_csv('../data/data7-2.csv',sep='|',names=['uid','oldprice','newprice'])
newDf=pd.merge(df1,df2,left_on='id',right_on='uid')
print(newDf,newDf.columns)

