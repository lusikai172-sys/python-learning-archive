import os

import requests

# 英雄列表接口链接
hero_url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2859429'
# 头部信息
hd = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/123'
}
data = requests.get(hero_url, headers=hd).json()['hero']  # 拿到英雄列表


def get_hero_skin(id, paths):
    """下载指定英雄的全部皮肤图片到 ./<英雄名>/ 目录。"""
    # 定义请求链接
    url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js?ts=2859284'.format(id)
    # 请求方式为 get；比较其他英雄的皮肤信息，得知 1 为 heroId
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/123'
    }
    res = requests.get(url, headers=headers)
    print(res.json())
    # 提取数据，找到 mainImg
    skins = res.json()['skins']
    for s in skins:
        print(s['mainImg'])
        if s['mainImg']:
            name = s['name']
            img_res = requests.get(s['mainImg'])
            print(img_res)
            # 有些 mainImg 为空，需要先判断再保存
            with open('./{}/{}.jpg'.format(paths, name), 'wb') as f:
                f.write(img_res.content)  # content 返回二进制内容


def mkdir_file(paths):
    """目录不存在则创建。"""
    if not os.path.exists('./' + paths):
        os.mkdir('./' + paths)
        print('创建文件成功', paths)
    else:
        print('已经存在该文件夹', paths)


if __name__ == '__main__':
    for hero in data:
        print(hero['heroId'])
        paths = hero['name']
        mkdir_file(paths)
        get_hero_skin(hero['heroId'], paths)
