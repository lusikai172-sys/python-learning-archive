from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

import pandas as pd

# 假设CSV文件结构正确，并且已经按照需求处理了
data = pd.read_csv('../classwork_02_weibo_hotsearch/微博热搜处理后.csv', names=['标题', '热度'])  # 确保列名正确

# 提取需要的数据
name = data['标题'].values.tolist()
number = data['热度'].values.tolist()

# Bar 图表
bar = (
    Bar()
        .add_xaxis(name)
        .add_yaxis('热度', number)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="微博热搜_Bar"),
        datazoom_opts=opts.DataZoomOpts(is_show=True)
    )
)

# Line 图表
line = (
    Line()
        .add_xaxis(name)
        .add_yaxis('热度', number)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="微博热搜_Line", pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%")
    )
)

# Grid 组合图
grid = (
    Grid()
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
)

# 保存 Grid 组合图为 HTML 文件
grid.render('组合图.html')