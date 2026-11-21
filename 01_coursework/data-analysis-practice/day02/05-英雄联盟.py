import requests
import os
# 英雄列表接口链接
hero_url='https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2858448'
# 头部信息
hd={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
data=requests.get(hero_url,headers=hd).json()['hero']
def get_hero_skin(id,paths):
    # 定义请求链接
    url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js?ts=2858446'.format(id)
    #    https://game.gtimg.cn/images/lol/act/img/js/hero/17.js?ts=2858448
    # 1  17  英雄的唯一标识，id

    # 构造请求
    res = requests.get(url, headers=hd)
    print(res.json())
    # 提取数据
    data = res.json()['skins']
    for s in data:
        print(s['mainImg'])
        if s['mainImg']:
            name = s['name'].replace('/','')
            img_res = requests.get(s['mainImg'])
            print(img_res)
            with open('./{}/{}.jpg'.format(paths,name), 'wb') as f:
                f.write(img_res.content)
def mkdir_file(paths):
#     先判断传进来的文件夹有没有存在
    if not os.path.exists('./'+paths):
#         如果没有则进行创建
        os.mkdir('./'+paths)
        print('创建文件成功',paths)
    else:
        print('已经有该文件夹了',paths)
for hero in data:
    print(hero['heroId'])
    paths=hero['name']
    mkdir_file(paths)
    get_hero_skin(hero['heroId'],paths)






