from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

v1 = ["鲁帆", "章戎", "王海强", "诸葛菠萝", "徐天宏", "张明"]
v2 = [25, 14, 12, 28, 8, 5]
v2 = sorted(v2)
c = (
     Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
    .set_global_opts(title_opts=opts.TitleOpts(title="不同人发送邮件数量"))
    .add("", [list(z) for z in zip(v1, v2)],radius=['10%', '70%'],center=['50%', '50%'],rosetype="radius")
#     .set_colors(
#         ['rgb({r},10,{b})'.format(r=255-20*(len(v2)-x+1), b=255-15*x) for x in range(len(v2))]
#     )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
c.render('环状饼图.html')
