import flask
from markupsafe import escape
# 利用escape进行转义
import flask_sqlalchemy as fs   # 包含操作数据库的类的模块
import os
import click
from faker import Faker


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')   # 配置SQL和数据库管理器
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监控
db = fs.SQLAlchemy(app)  # 利用SQLAlchemy类，操作数据库


# 创建表（用户名和电影）——利用类对象，继承自SQLAlchemy类，里面的属性就是表字段
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):  # 表名将会是 movie（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 在Flask中把对应函数名注册为flask命令（param_decls是补充参数）
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')


@app.cli.command()
def forge():
    db.create_all()
    fk = Faker()    # faker对象
    usr = User(name=fk.name())
    db.session.add(usr)
    movie_num = 10
    for _ in range(movie_num):
        movie = Movie(title=fk.street_name(), year=fk.year())
        db.session.add(movie)
    db.session.commit()


# 这里采用路径传参，在用户输入/user/xxxx时就把xxxx传给name.url/<参数名>，然后再视图函数中接收参数
# 也可以指定数据类型：/user/<string:name>
# string：默认使用此数据类型，接收没有任何斜杠"\/"的文本
# int：接收整形
# float：接收浮点型
# path：和string的类似，但是可以接受斜杠
@app.route('/user/<string:name>')
def user_page(name):
    return f"<h1>Hello {escape(name)}!</h1><img src='https://s.cn.bing.net/th?id=OHR.ConwyRiver_ZH-CN6871799250_1920x1080.webp&qlt=50&quot'>"


# get传参：url?参数=值，需使用flask的request.args来获取参数(from flask import request)
@app.route('/getvalue')
def use_parameters():
    arg = flask.request.args.get('number', 'param is wrong')
    return f"Parameter is {arg}"


@app.route('/')
def hello():
    return "Hello"


@app.route('/index')
def index():
    # name = 'JiLong'
    name = User.query.first().name
    # movies = [
    #     {'title': 'My Neighbor Totoro', 'year': '1988'},
    #     {'title': 'Dead Poets Society', 'year': '1989'},
    #     {'title': 'A Perfect World', 'year': '1993'},
    #     {'title': 'Leon', 'year': '1994'},
    #     {'title': 'Mahjong', 'year': '1996'},
    #     {'title': 'Swallowtail Butterfly', 'year': '1996'},
    #     {'title': 'King of Comedy', 'year': '1999'},
    #     {'title': 'Devils on the Doorstep', 'year': '1999'},
    #     {'title': 'WALL-E', 'year': '2008'},
    #     {'title': 'The Pork of Music', 'year': '2012'},
    #     {'title': 'lalala', 'year': '2024'}
    # ]
    movies = Movie.query.all()
    return flask.render_template('index.html', name=name, movies=movies)


# 访问测试URL，在控制台输出url_for()的值
@app.route('/test')
def test_url_for():
    # 测试带参数的url
    print(flask.url_for('user_page', name='jilong'))
    print(flask.url_for('user_page', name='haha'))
    print(flask.url_for('test_url_for'))
    print(flask.url_for('use_parameters'))
    return "<h1>This is for test 'url_for() func.'</h1>\nPlease check console!"


@app.route('/pic')
def show_pic():
    # 对于url_for()，如果endpoint='static'，另一个参数是filename，那么它会从static文件夹内寻找静态文件
    return f"<img src={flask.url_for(endpoint='static', filename='/images/jojo.png')}>"
