from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 数据准备
v1 = ["100000", "200000", "300000", "400000", "500000", "600000", "1000000", "1400000"]
v2 = [20, 12, 10, 2, 2, 2, 1, 1]

# 确保数据长度相同
assert len(v1) == len(v2), "列表 v1 和 v2 的长度必须相同"

# 创建饼图并设置主题
c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
    .set_global_opts(title_opts=opts.TitleOpts(title="热度比例"))
    .add("", [list(z) for z in zip(v1, v2)],
         radius=['10%', '70%'],
         center=['50%', '50%'])
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# 渲染饼图到 HTML 文件
c.render('环状饼图.html')
