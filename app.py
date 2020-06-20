from flask import Flask #从 flask 包导入 Flask 类
app = Flask(__name__)   #通过实例化这个类，创建一个程序对象 app



@app.route('/')      #一个视图函数可以绑定多个 URL，这通过附加多个装饰器实现
@app.route('/123')   #这个叫做装饰器，参数是对应的URL地址 (相对地址)
def hello():      #这个叫做与装饰器对应的视图函数，也叫请求处理函数
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    
    
from flask import escape
'''
escape 有摆脱、逃脱的意思。
注意:用户输入的数据会包含恶意代码，所以不能直接作为响应返回，
需要使用 Flask 提供的 escape() 函数对 name 变量进行转义处理，
比如把 < 转换成 &lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
'''

@app.route('/user/<name>')  #注意：变量放在一对箭头中间
def user_page(name):
    return 'User: %s' % escape(name)


from flask import url_for
'''
修改视图函数名？
首先，视图函数的名字是自由定义的，和 URL 规则无关。
和定义其他函数或变量一样，只需要让它表达出所要处理页面的含义即可。
除此之外，它还有一个重要的作用：作为代表某个路由的端点（endpoint），
同时用来生成 URL。对于程序内的 URL，为了避免手写，Flask 提供了一个 url_for 函数来生成 URL，
它接受的第一个参数就是端点值，默认为视图函数的名称.
'''
@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'