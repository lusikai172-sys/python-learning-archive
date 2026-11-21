import pandas as pd
from pyecharts.charts import Scatter3D #用于制作3d散点图
import pyecharts.options as opts

df = pd.read_csv('../classwork_02_weibo_hotsearch/微博热搜处理后.csv')
df.head()
df_select = df.loc[:100,['排名','标题','热度']]
x = df_select['排名'].tolist()
y = df_select['标题'].tolist()
z = df_select['热度'].tolist()
[[i,j,k] for i,j,k in zip(x,y,z)]
c = (
    Scatter3D()
    .add(
        '',
        data = [[i,j,k] for i,j,k in zip(x,y,z)], # 数据：二维数组
        xaxis3d_opts=opts.Axis3DOpts( # x轴配置
            name='排名',
            type_="value",
        ),
        yaxis3d_opts=opts.Axis3DOpts( # y轴配置
            name='标题',
            type_="value",
        ),
        zaxis3d_opts=opts.Axis3DOpts( # z轴配置
            name='热度',
            type_="value",
        ),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
                max_= max(z),
                range_color=[#图内小球具体颜色
                    "#1710c0",
                    "#0b9df0",
                    "#00fea8",
                    "#00ff0d",
                    "#f5f811",
                    "#f09a09",
                    "#fe0300",
                ],
        ),
    )
)
c.render('微博热搜散点图.html')