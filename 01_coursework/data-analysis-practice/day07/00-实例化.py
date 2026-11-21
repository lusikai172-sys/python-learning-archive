from pyecharts.charts import Bar
# 引入柱状图类
from pyecharts import options as opts
# 引入option配置
# 实例化
bar=Bar()
bar.add_xaxis(['衬衫','裤子','袜子','围巾'])
bar.add_yaxis('商家A',[5,30,50,100])
bar.add_yaxis('商家B',[15,3,54,66])
# set_global_opts  全局配置项
bar.set_global_opts(
#     标题配置
    title_opts=opts.TitleOpts(
        # 主标题名字
        title='淘宝大卖场',
        title_link='https://www.taobao.com',
        subtitle='销售量总结'
    ),
#     图例配置项
    legend_opts=opts.LegendOpts(
        is_show=True
    ),
#     工具箱配置项
    toolbox_opts=opts.ToolboxOpts(
        is_show=True
    ),
#     提示框配置项
    tooltip_opts=opts.TooltipOpts(
        background_color='pink',
        textstyle_opts=opts.TextStyleOpts(
            color='blue',
            font_size='66'
        )
    ),
#     区域缩放
    datazoom_opts=opts.DataZoomOpts(
        is_show=True
    ),
#     视觉映射
    visualmap_opts=opts.VisualMapOpts(
        is_show=True

    )
)
bar.render('商家信息.html')