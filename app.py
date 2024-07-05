from flask import Flask, render_template
from flask import url_for
from markupsafe import escape
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__) # 实例化一个flask对象


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # 实例化一个数据库对象


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


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