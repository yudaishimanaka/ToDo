# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, url_for, session, jsonify, redirect, json, make_response
from flaskext.mysql import MySQL
from flask_sslify import *
import lepl.apps.rfc3696
import json
import os
from passlib.hash import pbkdf2_sha256
from jinja2 import utils

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
email_validator = lepl.apps.rfc3696.Email()
mysql = MySQL()
app = Flask(__name__, template_folder=tmp_dir)
sslify = SSLify(app)
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
        name = str(utils.escape(request.json['name']))
        email = str(utils.escape(request.json['email']))
        password = pbkdf2_sha256.hash(request.json['pass'])
        if len(name) != 0 and len(email) != 0 and len(password) != 0:
            if email_validator(email):
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM User WHERE username = '" + name + "'")
                data = cursor.fetchone()
                if data is None:
                    cursor.execute('INSERT INTO User(username,email,password) VALUES(%s,%s,%s)',
                                   [name, email, password])
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
        name = str(utils.escape(request.form['name']))
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = '" + name + "'")
        data = cursor.fetchone()
        if data is None:
            error = "登録されていないユーザーです"
            session['msg'] = error
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(password, data[2]) is True:
                session['username'] = name
                return redirect(url_for('index'))
            else:
                error = "ユーザーネームまたはパスワードが間違っています"
                session['msg'] = error
                return redirect(url_for('login'))


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
        name = str(utils.escape(session['username']))
        title = str(utils.escape(request.json['title']))
        contents = str(utils.escape(request.json['contents']))
        level = request.json['level']
        period = request.json['period']
        period = period.split(" - ")
        status = request.json["status"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE username = '" + name + "'AND title ='" + title + "'")
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO Task (username,title,contents,startp,endp,level,status) '
                           'VALUES(%s,%s,%s,%s,%s,%s,%s)', [name, title, contents, period[0], period[1], level, status])
            conn.commit()
            return "タスクを登録しました!タスク一覧から確認してください！"
        else:
            return "タスク一覧または完了済みタスク一覧に同じタイトルのタスクが存在します"


@app.route("/request", methods=['GET'])
def request():
    from flask import jsonify, session
    name = str(utils.escape(session['username']))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task WHERE username = '" + name + "'AND status = 'on'")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)


@app.route("/update", methods=['POST'])
def update():
    from flask import request, jsonify
    if request.method == 'POST':
        name = str(utils.escape(request.json['name']))
        title = str(utils.escape(request.json['title']))
        status = request.json["status"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE "
                       "Task SET status ='" + status + "'WHERE username ='" + name + "'AND title ='" + title + "'")
        conn.commit()
        return "タスクは完了しました"


@app.route("/calendar")
def calendar():
    if 'username' not in session:
        return redirect(url_for('top'))
    else:
        return render_template("calendar.html")


@app.route("/tasklist", methods=['GET'])
def tasklist():
    from flask import jsonify, session
    name = str(utils.escape(session['username']))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task WHERE username = '" + name + "'AND status = 'on'")
    data = cursor.fetchall()
    response = []
    for value in range(len(data)):
        start = data[value][3]
        end = data[value][4]
        level = data[value][5]
        if level == "最重要":
            bgcolor = "#dd4b39"
            bodercolor = "#dd4b39"
        elif level == "重要":
            bgcolor = "#f39c12"
            bodercolor = "#f39c12"
        else:
            bgcolor = "#3c8dbc"
            bodercolor = "#3c8dbc"

        start = start.split("/")
        end = end.split("/")
        response.append({
            "title": data[value][1],
            "start": start[2] + "-" + start[0] + "-" + start[1],
            "end": end[2] + "-" + end[0] + "-" + end[1],
            "backgroundColor": bgcolor,
            "borderColor": bodercolor
        })
    cursor.close()
    return jsonify(response)


@app.route("/completed")
def completed():
    if 'username' not in session:
        return redirect(url_for('top'))
    else:
        return render_template("complete.html")


@app.route("/complist", methods=['GET'])
def complist():
    from flask import jsonify, session
    name = str(utils.escape(session['username']))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task WHERE username = '" + name + "'AND status = 'off'")
    data = cursor.fetchall()
    return jsonify(data)


@app.route("/remove", methods=['POST'])
def remove():
    from flask import request, jsonify
    if request.method == 'POST':
        name = str(utils.escape(request.json['name']))
        title = str(utils.escape(request.json['title']))
        print(title)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Task WHERE username ='" + name + "'AND title ='" + title + "'")
        conn.commit()
        return "タスクは削除されました"


@app.route("/setting")
def setting():
    if 'username' not in session:
        return redirect(url_for('top'))
    else:
        return render_template("setting.html")


@app.route("/register_endpoint", methods=['POST'])
def register_endpoint():
    from flask import request, jsonify
    if request.method == 'POST':
        name = str(utils.escape(request.json['name']))
        state = str(request.json['state'])
        endpoint = request.json['endpoint']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET "
                       "push_endpoint ='" + endpoint + "',push_state ='" + state + "' WHERE username ='" + name + "'")
        conn.commit()
        return "OK"


@app.route("/user_state", methods=['GET'])
def user_state():
    name = str(utils.escape(session['username']))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE username = '" + name + "'")
    data = cursor.fetchall()
    return jsonify(data)


@app.route("/update_state", methods=['POST'])
def update_state():
    from flask import request, jsonify
    if request.method == 'POST':
        name = str(utils.escape(request.json['name']))
        state = str(request.json['state'])
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET push_state ='" + state + "' WHERE username ='" + name + "'")
        conn.commit()
        return "OK"


@app.route("/fetch", methods=['POST'])
def fetch():
    from flask import request, jsonify
    if request.method == 'POST':
        endpoint = request.json['end_point']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE push_endpoint = '" + endpoint + "' AND push_state = 'True'")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM Task WHERE username = '" + data[0][0] + "' AND status = 'on'")
        push_data = cursor.fetchall()
        action = ""
        for i in range(len(push_data)):
            action += "・" + push_data[i][1] + "\n"

        if len(push_data) != 0:
            data = {
                "title": "僕だけのToDo管理",
                "body": "未完了タスクが" + str(len(push_data)) + "件あります!,ログインして確認しましょう!\n",
                "url": "https://todo.ydsteins.tk/login",
                "action": action
            }
            return jsonify(data)
        else:
            data = {
                "title": "僕だけのToDo管理",
                "body": "まずはタスクを登録してみましょう!",
                "url": "https://todo.ydsteins.tk/login",
                "action": ""
            }
            return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
