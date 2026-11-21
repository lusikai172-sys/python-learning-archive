from types import new_class

import tensorflow.compat.v1 as tf
# 禁用TensorFlow 2.x的即时执行模式，启用1.x的图执行模式
tf.compat.v1.disable_v2_behavior()


def tensorflow_demo():
    '''
    TensorFlow的基本结构
    :return:
    '''
    #原生python加法运算
    a = 2
    b = 3
    c = a + b
    print("普通加法运算的结果：\n",c)

    #TensorFlow实现加法运算
    a_t = tf.constant(2)
    b_t = tf.constant(3)
    c_t = a_t + b_t
    print("TensorFlow加法运算的结果：\n",c_t)


    #开启会话  在 TensorFlow 2.x 中启用 1.x 兼容模式
    with tf.Session(graph=tf.get_default_graph()) as sess:
        c_t_value = sess.run(c_t)
        print("c_t_value:\n",c_t_value)

    return None


def graph_demo():
    '''
    图的演示
    :return:
    '''
    #TensorFlow实现加法运算
    a_t = tf.constant(2,name="a_t")
    b_t = tf.constant(3,name="b_t")
    c_t = tf.add(a_t,b_t,name="c_t")
    print("a_t：\n",a_t)
    print("b_t：\n",b_t)
    print("c_t：\n",c_t)

    #查看默认图
    #方法1：调用方法
    default_g = tf.get_default_graph()
    print("default_g:\n",default_g)
    #方法2：查看属性
    print("a_t的图属性：\n",a_t.graph)
    print("c_t的图属性：\n", c_t.graph)

    #开启会话  在 TensorFlow 2.x 中启用 1.x 兼容模式
    with tf.Session() as sess:
        c_t_value = sess.run(c_t)
        print("c_t_value:\n",c_t_value)
        print("sess的图属性：\n", sess.graph)
        #1)将图写入本地生成events文件
        tf.summary.FileWriter("./tmp/summary",graph=sess.graph)

    #自定义图
    new_g = tf.Graph()
    #在自己的图中定义数据和操作
    with new_g.as_default():
        a_new = tf.constant(20)
        b_new = tf.constant(30)
        c_new = a_new + b_new
        print("a_new:\n",a_new)
        print("b_new:\n",b_new)
        print("c_new:\n",c_new)
        print("a_new的图属性：\n", a_new.graph)
        print("c_new的图属性：\n", c_new.graph)

    #开启会话  在 TensorFlow 2.x 中启用 1.x 兼容模式
    with tf.Session(graph=new_g) as new_sess:
        c_new_value = new_sess.run((c_new))
        print("c_new_value:\n",c_new_value)
        print("new_sess的图属性：\n", new_sess.graph)


    return None







if __name__ =="__main__":
    #代码1：TensorFlow的基本结构
    #tensorflow_demo()
    #代码2：图的演示
    graph_demo()

