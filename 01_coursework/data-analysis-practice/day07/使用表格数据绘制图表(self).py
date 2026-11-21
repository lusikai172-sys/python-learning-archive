import pandas as pd

# 因为CSV文件没有标题行，所以使用names参数指定列名
data = pd.read_csv('../day02/北京新发地.csv', names=['name', 'low', 'height', 'avg'])

# 提取需要的数据
name = data['name'].values.tolist()
price = data['avg'].values.tolist()

from pyecharts.charts import Bar
from pyecharts.options import ComponentTitleOpts, DataZoomOpts, TitleOpts

bar = (
    Bar()
        .add_xaxis(name)  # 直接使用列表name作为位置参数
        .add_yaxis('北京菜品信息', price)
        .set_global_opts(
        title_opts=TitleOpts(title="北京新发地菜品价格信息"),  # 设置图表标题
        datazoom_opts=DataZoomOpts(
            is_show=True
        )  # 设置数据区域缩放组件
    )
        .render('北京新发地.html')  # 渲染图表到HTML文件
)