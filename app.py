from flask import Flask, request, render_template, url_for, session, jsonify, redirect, json, make_response
from flaskext.mysql import MySQL
import lepl.apps.rfc3696
import json

email_validator = lepl.apps.rfc3696.Email()
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gurutaminn1009'
app.config['MYSQL_DATABASE_DB'] = 'todo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/")
def top():
    return render_template("top.html")


@app.route("/register", methods=['POST'])
def register():
    from flask import request
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        password = request.json['pass']
        if len(name) != 0 and len(email) != 0 and len(password) != 0:
            if email_validator(email):
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM User WHERE username = '" + name + "'")
                data = cursor.fetchone()
                if data is None:
                    cursor.execute('INSERT INTO User(username,email,password) VALUES(%s,%s,%s)', [name, email, password])
                    conn.commit()
                    return "登録できました！"
                else:
                    return "すでに同じユーザーネームのユーザーが存在します"
            else:
                return "正しいメールアドレスではありません"
        else:
            return "空のフィールドが存在します"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('msg', None)
    return redirect(url_for('login'))


@app.route("/index")
def index():
    if 'username' not in session:
        return redirect(url_for('top'))
    else:
        return render_template("index.html")


@app.route("/auth", methods=['POST'])
def auth():
    from flask import request
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = '" + name + "'AND password = '" + password + "'")
        data = cursor.fetchone()
        if data is None:
            error = "正しいユーザー名またはパスワードを入力してください"
            session['msg'] = error
            return redirect(url_for('login'))
        else:
            session['username'] = name
            return redirect(url_for('index'))


@app.route("/add")
def add():
    if 'username' not in session:
        return redirect(url_for('top'))
    else:
        return render_template("add.html")


@app.route("/taskadd", methods=['POST'])
def taskadd():
    from flask import request
    if request.method == 'POST':
        name = session['username']
        title = request.json['title']
        contents = request.json['contents']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE username = '" + name + "'AND title ='" + title + "'")
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO Task (username,title,contents) VALUES(%s,%s,%s)', [name, title, contents])
            conn.commit()
            return "タスクを登録しました!タスク一覧から確認してください！"
        else:
            return "すでに同じタスクが登録されていますs"


@app.route("/request", methods=['GET'])
def request():
    from flask import jsonify, session
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task WHERE username = '" + session['username'] + "'")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)


@app.route("/remove", methods=['POST'])
def remove():
    from flask import request, jsonify
    if request.method == 'POST':
        name = request.json['name']
        title = request.json['title']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Task WHERE username ='" + name + "'AND title ='" + title + "'")
        conn.commit()
        return "タスクは削除されました"


if __name__ == "__main__":
    app.run(debug=True)
