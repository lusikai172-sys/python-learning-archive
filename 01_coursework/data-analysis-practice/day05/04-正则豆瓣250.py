# 第一步，获取第一页网页源码并进行预处理
import requests
headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
url='https://movie.douban.com/top250'
res=requests.get(url,headers=headers)
content=res.text.replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace('&nbsp;','')
print(content)
# 第二步，从预处理好网页中提取我们需要标签，为之后提取做准备
import re
# 1.提取ol下面的所有li为一整个字符串
all_tags=re.findall('.*grid_view.*?(<li>.*</li>)',content)[0]
# 这一行中.*表示grid_view前可以是任意字符，这样就定位到class="grid_view"这个标签
# 第二个.*?表示grid_view和<li>之间可以是任意字符，遇见第一个<li>就停止了
# <li>.*</li>表示一个组，以<li>开头，以</li>结尾，中间采用贪婪模式匹配
# 如果最后li当中使用非贪婪，遇见第一个</li>就终止，则只有匹配到第一个li标签
print(all_tags)
# 2. 从所有的li中提取中每个li标签
movie_tags=re.findall('<li>.*?</li>',all_tags)
print(movie_tags)
print(len(movie_tags))
# 第三步,从所有的标签中提取出具体的内容
movie_info=[]
for movie in movie_tags:
    movie_name=re.findall('.*?class="title">(.*?)<',movie)[0]
    print(movie_name)
#     上映时间  上映地点 电影分类 电影评分
    other=re.findall('.*?class="bd".*?<br>(.*?)</p>',movie)[0]
    release_date=re.findall('\d+',other)[0]
    release_place=re.findall('.*?/(.*?)/',other)[0]
    release_category=re.findall('.*/(.*)',other)[0]
    movie_rate=re.findall('.*?rating_num.*?>(.*?)<',movie)[0]
    print(movie_rate)
    movie_info.append((movie_name,release_date,release_place,release_category,movie_rate))
# 第四步，将提取的内容组成一个元组添加到列表
# 第五步 获取要爬取的所有url,保存在列表中
# 第六步 遍历所有url，对每个url进行提取
# 第七步，保存所有数据


