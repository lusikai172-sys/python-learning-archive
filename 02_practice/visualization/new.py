import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("VIS_DATA_DIR", Path(__file__).resolve().parent / "data"))

from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

# 读取数据文件，将你的实际文件路径替换进去
data_path = DATA_DIR / "train_new2.csv"
df = pd.read_csv(data_path)

# 将start_time列转换为日期时间类型，方便后续处理
df['start_time'] = pd.to_datetime(df['start_time'])

# 提取小时信息，新增一个列存放小时数
df['hour'] = df['start_time'].dt.hour

# 按照小时进行分组，并统计每个小时的出行次数
hour_counts = df.groupby('hour').size()

# 实例化柱状图对象
bar = Bar(init_opts=opts.InitOpts(width="1000px", height="600px", theme="light"))  # 设置图表宽高与主题样式

# 设置横坐标，即0到23小时
bar.add_xaxis([str(i) + "时" for i in range(24)])

# 设置纵坐标，添加对应的数据系列，这里只一个系列表示出行次数
bar.add_yaxis("出行次数", hour_counts.tolist(),
              itemstyle_opts=opts.ItemStyleOpts(color="#5470C6"),  # 设置柱子颜色为蓝色系，可按需调整色值
              label_opts=opts.LabelOpts(is_show=True, position="top", font_size=12),  # 在柱子顶部显示数据标签
              markpoint_opts=opts.MarkPointOpts(  # 添加标记点展示特殊趋势信息
                  data=[
                      opts.MarkPointItem(type_="max", name="最大值"),  # 标记最大值点
                      opts.MarkPointItem(type_="min", name="最小值")  # 标记最小值点
                  ]
              )
              )

# 设置全局配置项
bar.set_global_opts(
    # 标题配置
    title_opts=opts.TitleOpts(
        title='汽车一天中各时刻出行次数统计',
        title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight='bold', color='#333')  # 优化标题字体样式
    ),
    # 图例配置项，这里图例就是数据系列的名称，设置显示图例，优化图例样式
    legend_opts=opts.LegendOpts(is_show=True, textstyle_opts=opts.TextStyleOpts(font_size=14, color='#666')),
    # 工具箱配置项，设置显示工具箱，方便进行一些交互操作，比如缩放、下载图片等
    toolbox_opts=opts.ToolboxOpts(is_show=True),
    # x轴配置项，调整坐标轴指针样式配置部分
    xaxis_opts=opts.AxisOpts(
        name='一天中的时刻',
        axislabel_opts=opts.LabelOpts(font_size=12, rotate=0),
        axispointer_opts=opts.AxisPointerOpts(
            is_show=True,
            type_="line",
            linestyle_opts=opts.LineStyleOpts(color="#ccc", width=1)
        )
    ),
    # y轴配置项，同样调整坐标轴指针样式配置部分
    yaxis_opts=opts.AxisOpts(
        name='出行次数',
        axislabel_opts=opts.LabelOpts(font_size=12),
        axispointer_opts=opts.AxisPointerOpts(
            is_show=True,
            type_="line",
            linestyle_opts=opts.LineStyleOpts(color="#ccc", width=1)
        ),
        splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(color='#eee'))
    )
)

# 渲染生成HTML文件，可在网页中打开查看图表
bar.render('car_trips_by_hour.html')