from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

# 读取CSV文件
df = pd.read_csv('../classwork_03_dangdang/当当预处理后.csv')

# 提取类别和值数据
categories = df['书名'].tolist()
values1 = df['线上价格'].tolist()
values2 = df['线下价格'].tolist()

# 创建Bar对象
bar = (
    Bar()
        .add_xaxis(categories)
        .add_yaxis("线上价格", values1, stack="stack1")
        .add_yaxis("线下价格", values2, stack="stack1")
        .set_global_opts(
        title_opts=opts.TitleOpts(title="价格对比"),
        legend_opts=opts.LegendOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        tooltip_opts=opts.TooltipOpts(
            background_color='blue',
            textstyle_opts=opts.TextStyleOpts(color='white', font_size='20')
        ),
        datazoom_opts=opts.DataZoomOpts(is_show=True),
        visualmap_opts=opts.VisualMapOpts(is_show=True),
    )
)

# 渲染图表到HTML文件
bar.render('对比.html')