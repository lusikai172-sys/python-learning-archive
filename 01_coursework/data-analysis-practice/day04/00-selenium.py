# 导入模块
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# 创建实例对象
# driver=webdriver.Chrome(executable_path='D:\python_project')
driver=webdriver.Chrome()
# 最大化窗口
driver.maximize_window()
# 创建chains实例对象
chains=ActionChains(driver)
url='https://www.baidu.com'
# 访问某个网址
driver.get(url)
# 查找输入框
kw=driver.find_element(by=By.ID,value='kw')
kw.send_keys('站长之家')
time.sleep(2)
# 查找百度一下
su=driver.find_element(by=By.ID,value='su')
# chains.click(su).perform()
chains.key_down(Keys.ENTER).perform()
# 获取result_logo
logo=driver.find_element(by=By.ID,value='result_logo')
chains.drag_and_drop(logo,kw).perform()
# suclick()
# 关闭当前页
# driver.quit()
print(driver.window_handles)
time.sleep(333)