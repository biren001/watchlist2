import os
import sys

sys.path.append('/Users/songyi/Documents/bianc/watchlist/env/lib/python3.8/site-packages/')
from flask import Flask #从 flask 包导入 Flask 类
app = Flask(__name__)   #通过实例化这个类，创建一个程序对象 app
from flask import render_template  ##从 flask 包导入 模板渲染函数
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from flask import request
from flask import flash
from flask import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user


#首页视图函数
app.route('/123')   #这个叫做装饰器，参数是对应的URL地址 (相对地址)
@app.route('/', methods=['GET', 'POST'])  #一个视图函数可以绑定多个 URL，这通过附加多个装饰器实现
def index():                              #这个叫做与装饰器对应的视图函数，也叫请求处理函数
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()   # 从数据库中读取用户记录
    movies = Movie.query.all()  # 从数据库中读取所有电影记录
    return render_template('index.html', user=user, movies=movies)  # A:渲染主页模板


#编辑电影条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


#删除电影条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


#404 错误处理函数
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码
'''
提示 和我们前面编写的视图函数相比，这个函数返回了状态码作为第二个参数，
普通的视图函数之所以不用写出状态码，
是因为默认会使用 200 状态码，表示成功。
'''


'''
模板上下文处理函数
对于多个模板内都需要使用的变量，
我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数，如下所示：
'''

@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}

'''
这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，
因此可以直接在模板中使用。
现在我们可以删除 404 错误处理函数和主页视图函数中的 user 变量定义，
并删除在 render_template() 函数里传入的关键字参数：
'''



#以下整块为数据库配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'  设置签名所需的密钥.这个密钥的值在开发时可以随便设置。
                                  # 基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍。

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  #数据库对象创建，但真正的数据库还没创建


#创建数据库模型类，也就是创建数据库中的表。分别是用户信息和电影条目信息。这是只是创建了类，正真的表还没创建。
'''
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）。其中模型类要声明继承 db.Model
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
'''    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


#模型类创建后，还不能对数据库进行操作，因为我们还没有创建真正的数据库文件和真正的表
#db.create_all() #创建真正的数据库，表也就跟着创建了
'''
#如果你改动了模型类，想重新生成表模型，那么需要先使用 db.drop_all() 删除表，但原来的数据库还在，
只是成了没有数据的空数据库，然后使用db.create_all() 重新创建新表。
注意：这会一并删除所有数据，如果你想在不破坏数据库内的数据的前提下变更表的结构，
需要使用数据库迁移工具，比如集成了 Alembic 的 Flask-Migrate 扩展。
'''

#创建命令来删除数据表并重建
import click

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
#在终端下，使用flask initdb 调用以上命令


#生成虚拟数据.创建自定义命令 forge
import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

#现在在终端执行 flask forge 命令就会把所有虚拟数据添加到数据库里：


#生成管理员账户
import click

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


#使用 Flask-Login 实现用户认证
login_manager = LoginManager(app)  # 实例化扩展类

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


#用户登录
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


#用户登出
@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


#设置用户名字
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


#使用 Python 标准库中的测试框架 unittest 来编写单元测试




'''
A:渲染主页模板
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
注意，数据虽然放在函数调用后面，但一样可以被调用,因为这两个是全局变量。
'''

'''
因为有另外一个函数提供了数据，所以此处屏蔽了
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
'''

'''
使用 SQLAlchemy 操作数据库
为了简化数据库操作，我们将使用 SQLAlchemy——一个 Python 数据库工具（ORM，即对象关系映射）。
借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），
通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。

Flask 有大量的第三方扩展，这些扩展可以简化和第三方库的集成工作。
我们下面将使用一个叫做 Flask-SQLAlchemy 的官方扩展来集成 SQLAlchemy。
'''

'''
以下为打印输出测试区域：
'''
import os
print("ccc")
print(os.path.join(app.root_path, 'data.db'))