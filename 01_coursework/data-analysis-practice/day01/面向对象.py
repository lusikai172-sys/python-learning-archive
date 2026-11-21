# 面向对象
# 以对象为主

class Student:
    # 类变量
    place='地球'
    # 类变量一般为不变的东西
    # 构造方法
    def __init__(self,name,age):
        # 成员变量
        self.name=name
        self.age=age
    def study(self):
        print("正在学习")

# 实例化
zhangsan=Student(name='张三',age=18)
zhangsan.study()
lisi=Student(name='李四',age=18)
lisi.study()