from bs4 import BeautifulSoup
# 创建bs4对象

html=open('06-前端简单了解.html','r',encoding='utf-8')
html=html.read()

soup=BeautifulSoup(html,'html.parser')
# html  页面源码     html.parser  解析器  html5lib lxml
print(type(soup))

'''
    把html转换为一个树状结构，每一个节点都是python对象，可以分为4中
    1. Tag    标签     name  attrs属性
    2. NavigateString      标签中的内容
    3. BeautifulSoup    soup对象
    4. Comment      注释内容
'''
print(soup.div.get('class'))
