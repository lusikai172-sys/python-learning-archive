import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_excel('../data/2020-2022疫情数据.xlsx')
print(df)
print(df.loc[0,'Q1':'Q4'])
# df.loc[0,'Q1':'Q4'].plot.bar()
# df.loc[0,'Q1':'Q4'].plot.barh()
df.groupby('team')['name'].count().plot.pie()
plt.show()