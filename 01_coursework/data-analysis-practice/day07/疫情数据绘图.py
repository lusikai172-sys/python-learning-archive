import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_excel('../day07/2020-2022疫情数据.xlsx')

print(df)

#print(df.loc[2,'date':'name'])  #2表示第三行
#print(df.loc[0:2,'date':'name'])  #0;2表示第一行到第三行
df.loc[0,'date':'name'].ploot().bar()
plot.show()