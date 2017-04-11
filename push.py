# -*- coding:utf-8 -*-
from flask import *
from flaskext.mysql import MySQL
import json
import requests

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gurutaminn1009'
app.config['MYSQL_DATABASE_DB'] = 'todo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
API_KEY = 'AAAA8dw0lcM:APA91bEP44rMh8Dnqp89LBhcmObcz4PCHSs5yxnoKZn99VqnWLXXWUDwl1kdEQPbmuWw6X_lckUgsUeSOL67gvuq8jVK_xXmHGXtQAEryFvakpe1MrhxGORScApCJ0i_KFmm4UOBWI4z'
url = 'https://fcm.googleapis.com/fcm/send'

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM User WHERE push_state = 'True'")
data = cursor.fetchall()
for i in data:
    id = i[3].replace("https://android.googleapis.com/gcm/send/", "")
    key = 'key=' + API_KEY
    fcm_header = {
        'Content-type': 'application/json; charset=UTF-8',
        'Authorization': key
    }
    body = {
        "data": {
            "title": "test",
            "body": "test",
            "url": "https://todo.ydsteins.tk/login"
        },
        "to": id
        }
    requests.post(url, data=json.dumps(body), headers=fcm_header)
