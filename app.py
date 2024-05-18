from flask import Flask, render_template
from flask import url_for
from markupsafe import escape
from faker import Faker

app = Flask(__name__) # 实例化一个flask对象


# 当访问根地址时，自动会调用该函数，并将返回值返回给视窗函数。
# @app.route('/')
# def hello():
#     return '''<h1>Welcome to my watchlist</h1><img src="http://helloflask.com/totoro.gif">'''


@app.route('/pic')
def load_pic():
    return '<img src="interlude_45.png">'


@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route('/test')
def test_url_for():
    """
    url_for()函数用来将一个
    :return:
    """
    print(url_for('load_pic'))
    return 'test'


"""
不能有重复的uri，每一个uri对应的页面必须唯一
"""
@app.route('/')
def index():
    """
    每次我们访问该地址时，都会调用一次该函数，进行动态渲染，然后把渲染结果返回出去作为网页的界面。
    :return: str
    """
    fake = Faker(locale='zh_CN')
    name = fake.name()
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    return render_template('index.html', name=name, movies=movies)


if __name__ == "__main__":
    app.run(debug=True)