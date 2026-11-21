import pandas as pd
df=pd.DataFrame(
    data={
        'name':['张三','李四','王二麻子'],
        'age':[12,3,46]
    }
)
# index=False  不写入索引
# header=False  不写入列名
# sep=','   设置分隔值
df.to_csv('write.csv',index=False,header=True,sep=',')
data=pd.read_csv('write.csv')
print(data)
