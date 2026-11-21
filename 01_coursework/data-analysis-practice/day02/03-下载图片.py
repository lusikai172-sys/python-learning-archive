from PIL import Image
# PIL python image library  第三方图像处理库
# Image类是PIL的核心类，包含很多方法，例如在文件中加载一张图像，处理其他形式的图像，从头创造一张图像...
# open   save   show
from io import BytesIO
# io.BytesIO   I/O类，用于在内存中读写二进制数据
import requests
# 请求链接
url='https://newlands-web.oss-cn-beijing.aliyuncs.com/img/202201061130.png'
# 构造请求
res=requests.get(url)
print(res.status_code)
print(res.content)
i=Image.open(BytesIO(res.content))
i.show()