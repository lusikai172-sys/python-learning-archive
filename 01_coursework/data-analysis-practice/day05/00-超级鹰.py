# 导入库
from selenium import webdriver
import time
# 导入超级鹰的类
from Chaojiying_Python.chaojiying import Chaojiying_Client
from selenium.webdriver.common.by import By
import time
# 创建driver
driver=webdriver.Chrome()
driver.get('http://pt.1000phone.com/userLogin')
img=driver.find_element(By.CSS_SELECTOR,'#app > div.bg.loginForSchool > div.content > div > form > div.el-form-item.authCode > div > img')
# 对需要识别的验证码进行截图保存，注意：文件名称最好为.png，否则会有警告
# 也可以获取img的src属性，请求链接获取二进制内容，或者使用src的base64字符串
img.screenshot('验证码.jpg')
# 读取截图的二进制内容
im=open('验证码.jpg','rb').read()
# 调用超级鹰生成实例对象，传入账号，密码，软件id(登录---用户中心---软件ID---生成一个软件ID使用软件Key即可)
chaojiying=Chaojiying_Client('harryminei','a123456','ab7dca01f6958e134e27820fcd43569b')
# 调用对象中的PostPic方法进行识别图片，传入图片信息和验证码类型 1902表示4-6为英文数字
cjy_res=chaojiying.PostPic(im,1902)
# 返回结果为一个json字符串，可以当成字典处理，其中pic_str为识别出的结果
print(cjy_res['pic_str'])
time.sleep(222)


