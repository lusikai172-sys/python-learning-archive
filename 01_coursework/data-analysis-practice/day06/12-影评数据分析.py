import pandas as pd
import matplotlib.pyplot as plt
# 获取数据
movie_data=pd.read_csv('../ml-1m/movies.dat',sep='::',names=['movie_id','movie_name','movie_type'],header=None,engine="python")
user_data=pd.read_csv('../ml-1m/users.dat',sep='::',names=['user_id','gender','age','occupation','zip-code'],header=None,engine="python")
rating_data=pd.read_csv('../ml-1m/ratings.dat',sep='::',names=['user_id','movie_id','rating','timestamp'],header=None,engine="python")
# print(movie_data.head())
# print(user_data)
# print(rating_data)
# 数据合并
movie_data['movie_id']=movie_data['movie_id'].astype(int)
df1=pd.merge(movie_data,rating_data)
# print(df1.columns)
movie=pd.merge(df1,user_data)
print(movie.head(),movie.columns)
# 查看有多少电影
# unique()  用于获取Series对象的唯一值，唯一性按出现顺序返回
print(movie['movie_name'].unique().size)
# 平均分较高的电影
# pivot_table()  可以指定行与列，对数据进行透视，计算出指定聚合值，并返回一个新的表格
# 四个重要的参数
# index  层次字段 要通过透视表获取什么信息就按照相应的顺序设置字段
# values  需要计算的数据，可以进行筛选
# aggfunc   设置对数据聚合时的函数操作，当未设置时，默认为mean
# columns  类似与index的层次字段，作为一个分割数据的可选方式
movie_rate_mean=pd.pivot_table(movie,values=['rating'],index=['movie_name'],aggfunc='mean')
print(movie_rate_mean.shape)
print(movie_rate_mean.head())
# inplace=True  不用打印输出，将内存中的数据删除，对内存有好处
movie_rate_mean.sort_values(by='rating',ascending=False,inplace=True)
print(movie_rate_mean[:20])
# 不同性别对电影评分
# 通过性别建立索引，再使用透视表分析数据
movie_gender_rating=pd.pivot_table(movie,values='rating',index=['movie_name'],columns=['gender'],aggfunc='mean')
print(movie_gender_rating.head(10))
# 不同性别争议最大的电影
# 男女评分差异：用女性的评分减去男性的评分得到差距
movie_gender_rating['diff']=movie_gender_rating.F-movie_gender_rating.M
print(movie_gender_rating.head())
movie_gender_rating.sort_values(by='diff',ascending=False,inplace=True)
f=movie_gender_rating[:10]
# 处理存在的NAN
m=movie_gender_rating.dropna()[-10:]
diff=pd.concat([f,m])
# diff.plot(y='diff',kind='barh',figsize=(16,9))
# plt.show()

# 为什么很多电影评分很高但是没听过，是因为评价人数少导致平均分很高，解决方案：加入评分限制来分析不同性别对电影的平均分
# 评价次数最多的50部中不同性别之间的打分差异
# 建议索引， 以name进行分组，统计出次数大小，排序，前50列
top_movie_name=movie.groupby('movie_name').size().sort_values()[::-1][:50].index
print(top_movie_name.size)
flag=movie_gender_rating.index.isin(top_movie_name)
df1=movie_gender_rating[flag].sort_values(by='diff')
print(df1.head())

# 不同年龄段争议最大的电影
movie['age'].plot(kind='hist',bins=20)
# plt.show()
print(movie.age.max())
# 将年龄分组
lables=['0-9','10-19','20-29','30-39','40-49','50-59']
movie['age-range']=pd.cut(movie['age'],bins=range(0,61,10),labels=lables)
print(movie.head())
print(movie.groupby('age-range')['rating'].mean())