from pyecharts import options as opts
# 导入地图类
from pyecharts.charts import Map

data=[
    ['武侯区',40],
    ['双流区',66],
    ['锦江区',20],
    ['龙泉驿区',134]
]
c=(
    Map()
    .add('商家A',data,"成都")
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='地图'
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            min_=20,
            max_=150,
            range_color=[
                'pink',
                'black',
                'red',
                'blue'
            ]
        )
    )
    .render('map1.html')
)