from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.globals import SymbolType
words = [
    ("牛肉面", 7800),
    ("黄河", 6181),
    ("《读者》杂志", 4386),
    ("甜胚子", 3055),
      ("五泉山", 2550)
]
c = WordCloud()
c.add("", words, word_size_range=[20, 80])
c.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-基本示例"))
c.render('词云图.html')