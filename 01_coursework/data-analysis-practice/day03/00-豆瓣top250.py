# 引入库
import requests
from bs4 import BeautifulSoup
import csv

# 创建爬取豆瓣的类
class DBSpider:
    # 初始化
    def __init__(self):
        # 成员变量
        self.url='https://movie.douban.com/top250?start={}&filter='
        # 头部信息
        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        # 代理ip列表
        self.proxieArray=['https://121.36.63.78:8118','https://121.36.63.78:8118']
        self.movieArr=[]   # 电音信息列表

    # 请求数据
    def getHtml(self):
        for page in range(10):
            try:
                # proxie={
                #     'https':self.proxieArray[0]
                # }
                res=requests.get(self.url.format(page*25),headers=self.headers)
                self.parseHtml(res.text)
            except Exception as e:
                print('异常处理',e)

    # 解析网页数据
    def parseHtml(self,html):
        soup=BeautifulSoup(html,'html.parser')
        info_list=soup.find('ol').find_all('li')
        for info in info_list:
            name=info.find('span',attrs={'class':'title'})
            rating_num=info.find('span',attrs={'class':'rating_num'})
            inq=info.find('span',attrs={'class':'inq'})
            if name!=None:
                name=name.text
            else:
                name=''
            if rating_num!=None:
                rating_num=rating_num.text
            else:
                rating_num=''
            if inq!=None:
                inq=inq.text
            else:
                inq=''
            str=info.find('p')
            if str!=None:
                year=str.text.split('.')[-1].split('/')[0].strip()
                director=str.text.split('导演: ')[-1].split(' ')[0]
            else:
                year=''
                director=''
            movies={}
            movies['电影名称']=name
            movies['评分']=rating_num
            movies['上映时间']=year
            movies['评语']=inq
            self.movieArr.append(movies)
    # 存储数据
    def saveHtml(self):
        file_obj=open('豆瓣250.csv','w',encoding='utf-8',newline='')
        csv_obj=csv.writer(file_obj)
        csv_obj.writerow(['电影名称','评分','上映时间','评语'])
        for i in self.movieArr:
            csv_obj.writerow([i['电影名称'],i['评分'],i['上映时间'],i['评语']])
    # 启动函数
    def run(self):
        self.getHtml()
        self.saveHtml()

DBSpider().run()