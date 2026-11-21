import pandas as pd
# 向前向后填充缺失值
df1=pd.DataFrame(
    [[10,20,30],[],[55,15,12],[44,12,7,12],[44,12],[55,15,7,12]],
    columns=['a','b','c','d'],
    index=['one','two','three','four','five','six']
)
print(df1)
print(df1.ffill())
print(df1.bfill())