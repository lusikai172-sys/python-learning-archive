from pyecharts import options as opts
from pyecharts.charts import Geo

data = [
    ('广东省', 40),
    ('四川省', 66),
    ('上海市', 20),
    ('浙江省', 134),
    ('湖南省', 88)
]

c = (
    Geo()
        .add_schema(maptype="china")
        .add("商家A", data)
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
        .render("map1.html")
)