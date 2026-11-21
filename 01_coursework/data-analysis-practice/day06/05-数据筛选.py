import pandas as pd
df=pd.read_csv('../data/data1.csv',sep=',')
# print(df)
# print(df[df['price']>2000])
# print(df[df.price.between(3000,4000)])
# #  & 与   |  或  ~ 非
# print(df[~df.price.between(3000,4000)])
# na=False   赋值
print(df[df.value.str.contains('苹果',na=True)])