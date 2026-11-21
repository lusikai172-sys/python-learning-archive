from pyecharts.charts import *
from pyecharts import options as opts
import pandas as pd
data=pd.read_csv('../day02/北京新发地.csv',names=['name','low','height','avg'])
print(data)
x=data['name'].values.tolist()
y1=data['low'].values.tolist()
y2=data['height'].values.tolist()

bar=Bar(init_opts=opts.InitOpts(
    theme='light',
    width='1000px',
    height='600px'
))
bar.add_xaxis(x)
# bar.extend_axis(yaxis=opts.AxisOpts())
bar.add_yaxis('最低价',y1,yaxis_index=0)
line=Line(init_opts=opts.InitOpts(
    theme='light',
    width='1000px',
    height='600px'
))
line.add_xaxis(x)
line.add_yaxis('最高价',y2)
bar.overlap(line)
bar.set_global_opts(
    datazoom_opts=opts.DataZoomOpts(
        is_show=True
    )
)
bar.render('对比.html')

