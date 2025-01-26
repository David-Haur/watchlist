import flask
from markupsafe import escape
# 利用escape进行转义
import flask_sqlalchemy as fs   # 操作数据库的类
import os


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
db = fs.SQLAlchemy(app)


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
    name = 'JiLong'
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
        {'title': 'lalala', 'year': '2024'}
    ]
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


if __name__ == '__main__':
    print('sqlite:////' + os.path.join(app.root_path, 'data.db'))
