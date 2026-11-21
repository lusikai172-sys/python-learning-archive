import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Timeline
from pyecharts import options as opts
# 读取数据
df=pd.read_excel('2020-2022疫情数据.xlsx')
# print(df.head())
# print(df.columns)
# print(df.tail())
df1=df.copy()
df1['month']=pd.DatetimeIndex(df1['date']).month
df1['year']=pd.DatetimeIndex(df1['date']).year
df1['year']=df1['year'].astype(str)
df1['month']=df1['month'].astype(str)
df1['year-month']=df1['year']+'_'+df1['month']
print(df1.head())
print(df1.tail())
data=pd.pivot_table(df1,values='total_confirm',index=['name'],columns=['year'],aggfunc='mean')
print(data)
t=Timeline()
# 讲解事件线，根据不同的时间线展示对应的数据
# for month in df1['month'].unique():
#     df_month=df1[df1['month']==month]
print(df1['name'].unique().tolist(),'---------')
bar=(
        Bar()
        .add_xaxis(df1['name'].unique().tolist())
        .add_yaxis('2020年数据',data['2020'].values.tolist())
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(
                is_show=True
            )
        )
        .render('test.html')
)
    # t.add(bar,f"{month}月")
    # t.render('test.html')
#     根据name获取每年的平均分
#     根据年月分组获取平均分

