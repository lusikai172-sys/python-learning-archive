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
        .add_xaxis(score)  # 直接使用列表name作为位置参数
        .add_yaxis('数量', number)
        .set_global_opts(
        title_opts=TitleOpts(title="猫眼Top100不同分数的电影数量"),  # 设置图表标题
        datazoom_opts=DataZoomOpts(
            is_show=True
        )  # 设置数据区域缩放组件
    )
        .render('猫眼Top100不同分数的电影数量.html')  # 渲染图表到HTML文件
)