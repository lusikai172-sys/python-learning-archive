from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

import pandas as pd

# 假设CSV文件结构正确，并且已经按照需求处理了
data = pd.read_csv('../classwork_03_dangdang/当当预处理后.csv')

# 提取需要的数据
name = data['书名'].values.tolist()
price = data['线上下价格差距'].values.tolist()

# Bar 图表
bar = (
    Bar()
        .add_xaxis(name)
        .add_yaxis('线上下价格差距', price)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="线上下价格差距_Bar"),
        datazoom_opts=opts.DataZoomOpts(is_show=True)
    )
)

# Line 图表
line = (
    Line()
        .add_xaxis(name)
        .add_yaxis('线上下价格差距', price)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="线上下价格差距_Line", pos_top="48%"),
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