# 导入库
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from Chaojiying_Python.chaojiying import Chaojiying_Client
# 创建一个爬虫类
class my_spider:
    # 构造方法
    def __init__(self):
        self.url='https://study.xiaoe-tech.com/t_l/learnLogin#/acount'
        self.driver=webdriver.Chrome()
        self.wait=WebDriverWait(self.driver,50)
        self.driver.maximize_window()

    def wait_element(self,type,value):
        self.wait.until(Ec.presence_of_element_located(((type,value))))
        return self.driver.find_element(type,value)
    def get_html(self):
        # 访问网站
        self.driver.get(self.url)
        # //*[@id="common_template_mounted_el_container"]/div/div[1]/div[3]/div/div[1]/p[2]
        type=By.XPATH
        #  点击密码登录
        pw_Login=self.wait_element(type,'//*[@id="common_template_mounted_el_container"]/div/div[1]/div[3]/div/div[1]/p[2]')
        pw_Login.click()
        # 账号输入
        username = self.wait_element(type,'//*[@id="common_template_mounted_el_container"]/div/div[1]/div[3]/div/div[3]/div/div[1]/div[1]/div/div[2]/input')
        username.send_keys('12345678904')
        # 密码输入
        password = self.wait_element(type,'//*[@id="common_template_mounted_el_container"]/div/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div/div/input')
        password.send_keys('234')
        # 点击登录
        login = self.wait_element(type,'//*[@id="common_template_mounted_el_container"]/div/div[1]/div[3]/div/div[3]/div/div[2]')
        login.click()
        # //*[@id="slideBg"]   获取图片
        # 切换到嵌套页面中 tcaptcha_iframe
        time.sleep(3)
        self.driver.switch_to.frame('tcaptcha_iframe')
        img = self.wait_element(type,'//*[@id="slideBg"]')
        # 获取图片二进制内容
        content=requests.get(img.get_attribute('src')).content
        # //*[@id="tcaptcha_drag_thumb"]
        #   获取鼠标起始位置的标签
        begin=self.driver.find_element(By.XPATH,'//*[@id="tcaptcha_drag_thumb"]')
        # 识别图片获取鼠标结束位置的x坐标
        self.get_num(content)
        # 操作鼠标
        chains=ActionChains(self.driver)
        # 动作1：起始位置按住鼠标不放
        chains.click_and_hold(begin).perform()
        # 动作2：移动鼠标至某个位置
        #   // 地板除  5//2=2    5//3=1
        chains.move_by_offset(int(self.x)//2,0).perform()
        chains.move_by_offset(-50,0).perform()
        time.sleep(2)
        # 动作3：松开鼠标
        chains.release().perform()
        time.sleep(222)
    def get_num(self,content):
        chaojiying=Chaojiying_Client('harryminei','a123456','ab7dca01f6958e134e27820fcd43569b')
        res=chaojiying.PostPic(content,9101)
        self.x=res['pic_str'].split(',')[0]
spider=my_spider()
spider.get_html()