from pyecharts import options as opts
from pyecharts.charts import Page, Pie
L1=['教授','副教授','讲师','助教','其他']
num  = [20,30,10,12,8]
c = Pie()
c.add("", [list(z) for z in zip(L1,num)])
c.set_global_opts(title_opts=opts.TitleOpts(title="Pie-职称类别比例"))
c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
c.render('饼图.html')