import pandas as pd
df=pd.DataFrame(
    data={
        'name':['张三','李四','王二麻子','王二麻子','王二麻子','王二麻子'],
        'age':[12,3,46,1,2,3]
    }
)
print(df.head(1))   # 默认查看前5条数据，可以指定数量
print(df.tail(2))  # 查看后2条
print(df.sample(3))  # 随机查看几条数据
print(df.shape)  # 查看行数列数
print('-------')
print(df.info)   # 查看索引、数据类型和内存信息
print(df.describe())  # 查看数值型列的汇总统计
print(df.dtypes)  #查看各字段的类型
print(df.axes)  # 显示数据行聚合列名
print(df.columns)  #  列名
