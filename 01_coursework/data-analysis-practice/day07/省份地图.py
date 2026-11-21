from pyecharts import options as opts
from pyecharts.charts import Geo

data = [
    ('成都市', 40),
    ('乐山市', 66),
    ('南充市', 20),
    ('绵阳市', 134)
]

c = (
    Geo()
        .add_schema(maptype="四川")
        .add("商家A", data,'四川')
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="中国地图"
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            min_=20,
            max_=150,
            range_color=[
                'yellow',
                'orange',
                'red'
            ]
        ),
    )
        .render("map2.html")
)