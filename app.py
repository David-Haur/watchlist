from flask import Flask
from flask import url_for
from  markupsafe import escape

app = Flask(__name__) # 实例化一个flask对象


# 当访问根地址时，自动会调用该函数，并将返回值返回给视窗函数。
@app.route('/')
def hello():
    return '''<h1>Welcome to my watchlist</h1><img src="http://helloflask.com/totoro.gif">'''


@app.route('/pic')
def load_pic():
    return '<img src="interlude_45.png">'


@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route('/test')
def test_url_for():
    print(url_for('load_pic'))
    return 'test'


if __name__ == "__main__":
    app.run(debug=True)