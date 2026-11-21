from pyecharts import options as opts
from pyecharts.charts import Scatter
week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
c = Scatter()
c.add_xaxis(week)
c.add_yaxis("商家A", [81,65,48,32,68,92,87])
c.set_global_opts(title_opts=opts.TitleOpts(title="Scatter-一周的销售额（万元）"))
c.render('散点图.html')

