from pyecharts.charts import Bar
#引入柱状图类
from pyecharts import options as opts
#引入option配置

#实例化
bar=Bar()
bar.add_xaxis(['衬衫','裤子','袜子','围巾'])  #横坐标的设定
bar.add_yaxis('商家A',[5,30,50,100])  #纵坐标的设定
bar.set_global_opts()
bar.render('商家信息新.html')