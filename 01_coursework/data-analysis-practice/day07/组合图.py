from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line,Scatter
A = ["小米", "三星", "华为", "苹果", "魅族", "VIVO", "OPPO"]
CA = [100,125,87,90,78,98,118]
B = ["草莓", "芒果", "葡萄", "雪梨", "西瓜", "柠檬", "车厘子"]
CB = [78,95,120,102,88,108,98]
bar = Bar()
bar.add_xaxis(A)
bar.add_yaxis("商家A",CA)
bar.add_yaxis("商家B", CB)
bar.set_global_opts(title_opts=opts.TitleOpts(title="Grid-Bar"))
bar.render_notebook()
line=Line()
line.add_xaxis(B)
line.add_yaxis("商家A", CA)
line.add_yaxis("商家B", CB)
line.set_global_opts(title_opts=opts.TitleOpts(title="Grid-Line", pos_top="48%"),
legend_opts=opts.LegendOpts(pos_top="48%"))
line.render_notebook()
grid = Grid()
grid.add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
grid.add(line, grid_opts=opts.GridOpts(pos_top="60%"))
grid.render('组合图.html')