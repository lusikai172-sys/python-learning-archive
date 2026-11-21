import requests
from bs4 import BeautifulSoup
# 创建王者爬虫类
class wzrySkinSpider():
    # 初始化
    def __init__(self):
        # 创建公用的数据
        self.hero_url='https://pvp.qq.com/web201605/herodetail/{}.shtml'
        self.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        self.herolist_url='https://pvp.qq.com/web201605/herolist.shtml'
    # 封装请求的函数
    def request_get(self,url,hd):
        res=requests.get(url,headers=hd)
        res.encoding='gbk'
        return res
    # 封装保存图片的函数
    def save_file(self,content,filename):
        # 保存皮肤图片
        with open('{}.jpg'.format(filename),'wb') as f:
            f.write(content)
    # 解析英雄列表页，提取所有英雄id
    def herolist_parse(self,html):
        soup=BeautifulSoup(html,'html.parser')
        herolist_content=soup.find('div',attrs={'class':'herolist-content'}).find_all('a')
        heroid_list=[]
        for hero in herolist_content:
            href=hero['href']
            heroid=href.split('/')[-1].split('.')[0]
            print(heroid)
            heroid_list.append(heroid)
        return heroid_list
    # 解析页面函数
    def hero_parse(self,html,ids):
        soup=BeautifulSoup(html,'html.parser')
        pic=soup.find('div',attrs={'class':'pic-pf'}).ul
        imgName=pic['data-imgname']
        names=imgName.split('|')
        names=[j.split('&')[0] for j in names]
        print(names)
    #     根据获取到的列表长度生成数字列表进行循环，将数字拼接在图片链接中
        for i in range(1,len(names)+1):
            url='https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(ids,ids,i)
            img_res=self.request_get(url,self.headers)
            skinname=names[i-1]
            # 调用保存函数，传递二进制内容和文件名称
            self.save_file(img_res.content,skinname)
    # 启动函数
    def run(self):
        # 请求链接函数调佣
        hero_res=self.request_get(self.herolist_url,self.headers)
        # 解析页面函数调用
        herolist_id=self.herolist_parse(hero_res.text)
        for ids in herolist_id:
#             请求所有单个英雄的详情链接
            res=self.request_get(self.hero_url.format(ids),self.headers)
#             调用解析单个英雄页面的函数
            self.hero_parse(res.text,ids)
wzry=wzrySkinSpider()
wzry.run()