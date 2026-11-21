from pyecharts.charts import Bar
#引入柱状图类
from pyecharts import options as opts
#引入option配置

import pandas as pd

# 因为CSV文件没有标题行，所以使用names参数指定列名
data = pd.read_csv('../classwork_01_maoyan_top100/不同分数的电影数量.csv', names=['score', 'number'])

# 提取需要的数据
score = data['score'].values.tolist()
number = data['number'].values.tolist()

from pyecharts.charts import Bar
from pyecharts.options import ComponentTitleOpts, DataZoomOpts, TitleOpts
bar = (
    Bar()
        .add_xaxis(score)  # 直接使用列表score作为位置参数
        .add_yaxis('数量', number)
        .set_global_opts(
        title_opts=opts.TitleOpts(
            #主标题名字
            title="猫眼Top100不同分数的电影数量",
            title_link='https://m.maoyan.com/asgard/board/4',
            subtitle='Top100'
        ),  # 设置图表标题
        #图例配置项
        legend_opts=opts.LegendOpts(
            is_show=True
        ),
        #工具箱配置项
        toolbox_opts=opts.ToolboxOpts(
            is_show=True
        ),
        #提示框配置项
        tooltip_opts=opts.TooltipOpts(
            background_color='blue',  #设置背景框颜色
            textstyle_opts=opts.TextStyleOpts(
                color='white', #设置字体颜色
                font_size='66'
            )
        ),
        #区域缩放
        datazoom_opts=opts.DataZoomOpts(
            is_show=True
        ),
        #视觉映射
        visualmap_opts=opts.VisualMapOpts(
            is_show=True
        )
    )
        .render('猫眼Top100不同分数的电影数量.html')  # 渲染图表到HTML文件
)
