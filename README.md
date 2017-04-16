# ToDo
PythonのFlaskというWebフレームワークを用いいて書かれたToDo管理

## 環境
Python3.~,pip,gitがインストールされている環境

## ダウンロード
```bash
$ git clone git@github.com:yudaishimanaka/ToDo.git
```

## 設定
ローカル用に設定ファイル名の変更
```bash
$ cd ToDo
$ mv my.cfg.sample my.cfg
```
my.cfgの変数を設定する
```python
DEBUG=True
MYSQL_DATABASE_USER='your mysql root user' < ローカルDBのrootユーザー
MYSQL_DATABASE_PASSWORD='your mysql root password' < rootユーザーのパスワード
MYSQL_DATABASE_DB='todo'
MYSQL_DATABASE_HOST='localhost'
API_KEY='your FCM or GCM secret key(server key)' < FCMまたはGCMで取得したAPI_KEY(Serverkey)
```

パッケージのインストール
```bash
pip install -r requirements.txt
```

## 起動
サーバー起動
```bash
python app.py
```

http://localhost:5000 でアクセス
