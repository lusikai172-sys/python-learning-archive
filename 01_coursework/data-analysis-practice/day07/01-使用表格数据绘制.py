import pandas as pd
data=pd.read_csv('../day02/北京新发地.csv',names=['name','low','height','avg'])
print(data)
name=data['name'].values.tolist()
price=data['avg'].values.tolist()
from pyecharts.charts import Bar
import pyecharts.options as opts
bar=(
    Bar()
    .add_xaxis(name)
    .add_yaxis('北京菜品信息',price)
    .set_global_opts(
        datazoom_opts=opts.DataZoomOpts(
            is_show=True
        )
    )
    .render('北京新发地.html')
)