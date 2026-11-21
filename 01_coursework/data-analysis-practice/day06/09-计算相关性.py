import pandas as pd

df1=pd.DataFrame(
    [[10,20,30,40],[7,14,21,28],[55,15,7,12],[44,12,7,12],[44,15,7,12],[55,15,7,12]],
    columns=['a','b','c','d'],
    index=['one','two','three','four','five','six']
)
print(df1.corr())
df2=pd.DataFrame(
    [[11,340,356,400],[70,154,211,328],[595,165,27,112],[44,12,7,12],[44,15,7,12],[55,15,7,12]],
    columns=['a','b','c','d'],
    index=['one','two','three','four','five','six']
)
print(df2.corrwith(other=df1))