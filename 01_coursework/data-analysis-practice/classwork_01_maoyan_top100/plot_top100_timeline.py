import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

# 读取CSV文件
data = pd.read_csv('../classwork_01_maoyan_top100/按时间顺序排列的top100电影（附链接）.csv', encoding='GBK')

# 提取需要的数据
title_list = data['title'].tolist()
year_time_list = data['year_time'].astype(str).tolist()
rank_list = data['rank'].tolist()  # 电影得分的排名

# 创建散点图
scatter = (
    Scatter()
        .add_xaxis(year_time_list)
        .add_yaxis("得分排名", rank_list)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="猫眼Top100电影情况一览",
                title_link="https://m.maoyan.com/asgard/board/4",
                subtitle="Top100电影"
            ),
            legend_opts=opts.LegendOpts(is_show=True),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(
                background_color="yellow",
                textstyle_opts=opts.TextStyleOpts(
                    color="white",
                    font_size="20"
                )
            ),
            datazoom_opts=opts.DataZoomOpts(is_show=True),

            visualmap_opts=opts.VisualMapOpts(
                is_show=True
            )
        )
        .render('猫眼Top100电影情况.html')  # 渲染图表到HTML文件
)
