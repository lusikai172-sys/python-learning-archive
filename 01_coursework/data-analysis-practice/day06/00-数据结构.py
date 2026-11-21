from pandas import Series
#
# s1=Series(
#     data=['尼古拉斯','爱新觉罗','法外狂徒','维多利亚'],
#     index=['a','b','c','d']
# )
# print(s1,type(s1))
# # 查询
# print(s1['a'])
# print(s1[0])
# # 使用默认索引依旧由左闭右开
# print(s1[0:2])
# # 使用自定义索引则没有左闭右开
# print(s1['a':'c'])
# # 新增
# s1=s1._append(Series(data=['伊丽莎白'],index=['e']))
# print(s1)
# # 删除
# s1=s1.drop('a')
# print(s1)
# print(s1.index,s1.values)

# s2=Series(
#     data=[
#         {'name':"尼古拉斯",'nickname':'赵四'},
#         {'name': "尼古拉斯", 'nickname': '赵四'},
#         {'name': "尼古拉斯", 'nickname': '赵四'},
#     ],
#     index=[1,2,3]
# )
# print(s2)
# s3=Series(
#     data={'name': "尼古拉斯", 'nickname': '赵四'}
# )
# print(s3)
import pandas as pd
df=pd.DataFrame(
    data={
        '上单':['吕布','花木兰','老夫子','海诺'],
        '中单':['小乔','王昭君','貂蝉','西施'],
        '辅助':['东皇','刘婵','牛魔王','盾山'],
        '打野':['娜可露露','韩信','李白','澜'],
        '射手':['马可波罗','鲁班','狄仁杰','公孙离']
    },
    index=['a','b','c','d']
)
print(df,type(df))
# 按照单列
# print(df['上单'],type(df['上单']))
# # 单行   不行
# # print(df['a'])
# # print(df[0])
# # 范围  多行
# print(df[0:2])
# # 多列  不行
# print('-----------------------')
# print(df['上单':'辅助'])

'''
行
    行索引名称
    行下标位置
列
    列索引名称
    列下标位置

loc 
    主要以索引名称进行查询
iloc
    主要以下标位置进行查询
    
    先行后列
    [行,列]
'''
# 单行单列
# print(df.loc['a','中单'])
# # 单行多列
# print(df.loc['a','上单':'辅助'])   # 按照范围
# print(df.loc['a',['上单','辅助']])   # 单独提取某几个列
# # 多行单列
# print(df.loc['a':'c','辅助'])
# print(df.loc[['a','c'],'辅助'])
# # 多行多列
# print(df.loc[['a','b'],['中单','打野']])
# print(df.loc['d',:])
# print(df.iloc[3,2])
# print(df.iloc[1,[0,3]])

