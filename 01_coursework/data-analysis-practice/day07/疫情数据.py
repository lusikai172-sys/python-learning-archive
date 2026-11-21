import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Timeline   #时间线展示数据
from pyecharts import options as opts
#读取数据
df=pd.read_excel('2020-2022疫情数据.xlsx')
print(df.head())
print(df.columns)
print(df.tail())
df1=df.copy()
df1['month']=pd.DatetimeIndex(df1['date']).month
df1['year']=pd.DatetimeIndex(df1['date']).year
df1['year']=df1['year'].astype(str)
df1['month']=df1['month'].astype(str)
df1['year-month']=df1['year']+'_'+df1['month']   #字符串之间进行拼接
print(df1.head())  #前五条
print(df1.tail())  #后五条

t=Timeline()
#讲解时间线，根据不同的时间线展示对应的数据
for month in df1['month'].unique():
    df_month=df1[df1['month']==month]
    bar=(
        Bar()
        .add_xaxis(df_month['name'].tolist())  #tolist()是转化成列表的意思
        .add_yaxis(df_month.columns[1],df_month['total_confirm'].tolist())
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(
                is_show=True
            )
        )
    )
    t.add(bar,f"{month}月")
    t.render('test.html')
