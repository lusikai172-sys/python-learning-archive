import pandas as pd
# data=pd.read_csv('../data/data1.csv')
# # 去重
# data=data.drop_duplicates()
# print(data)
df=pd.DataFrame(
    {
        'age':[30,30,22,13,13,50,22],
        'height':[123,123,165,163,80,129,126],
        'Score':[4.6,4.6,4.6,2.7,1.8,3.5,6.7],
        'State':['NY','NY','GF','SD','SD','QW','QW']
    },
    index=['a','a','a','d','e','f','g']
)
print(df)
df=df.drop_duplicates()
print(df)
data=pd.read_csv('../data/data2.csv')
print(data)
data['name']=data['name'].str.replace('J','K').str.strip()
print(data)