from flask import Flask #从 flask 包导入 Flask 类
app = Flask(__name__)   #通过实例化这个类，创建一个程序对象 app
from flask import render_template  ##从 flask 包导入 模板渲染函数


@app.route('/')      #一个视图函数可以绑定多个 URL，这通过附加多个装饰器实现
@app.route('/123')   #这个叫做装饰器，参数是对应的URL地址 (相对地址)
def index():      #这个叫做与装饰器对应的视图函数，也叫请求处理函数
    return render_template('index.html', name=name, movies=movies)

    
'''
渲染主页模板
使用 render_template() 函数可以把模板渲染出来，必须传入的参数为模板文件名
（相对于 templates 根目录的文件路径），
这里即 'index.html'。为了让模板正确渲染，我们还要把模板内部使用的变量通过关键字参数传入这个函数
'''

'''
在传入render_template() 函数的关键字参数中，左边的 movies 是模板中使用的变量名称，
右边的 movies 则是该变量指向的实际对象。这里传入模板的 name 是字符串，movies 是列表，
但能够在模板里使用的不只这两种 Python 数据结构，你也可以传入元组、字典、函数等。
render_template() 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句，
返回渲染好的模板内容。在返回的页面中，变量会被替换为实际的值（包括定界符），
语句（及定界符）则会在执行后被移除（注释也会一并移除）。
'''
 
    
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



'''
Jinja2 的语法和 Python 大致相同，你在后面会陆续接触到一些常见的用法。
在模板里，你需要添加特定的定界符将 Jinja2 语句和变量标记出来，
下面是三种常用的定界符：
{{ ... }} 用来标记变量。
{% ... %} 用来标记语句，比如 if 语句，for 语句等。
{# ... #} 用来写注释。
模板中使用的变量需要在渲染的时候传递进去，具体我们后面会了解。
'''

'''
{# 使用 length 过滤器获取 movies 变量的长度 #}
<p>{{ movies|length }} Titles</p>

为了方便对变量进行处理，Jinja2 提供了一些过滤器，语法形式如下：
{{ 变量|过滤器 }}
左侧是变量，右侧是过滤器名。比如，上面的模板里使用 length 过滤器来获取 movies 的长度，
类似 Python 里的 len() 函数。
提示 访问 http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters
查看所有可用的过滤器。
'''

'''
准备虚拟数据
为了模拟页面渲染，我们需要先创建一些虚拟数据，用来填充页面内容：
注意，数据虽然放在函数调用后面，但一样可以被调用。
'''

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]