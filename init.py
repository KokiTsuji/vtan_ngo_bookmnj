from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmnj.db"  # データベースの場所を指定
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)  # データベースに接続

# データベースモデル定義

class Lending(db.Model):
    __tablename__ = "lending"
    lendid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    bookname = db.Column(db.String(80))
    school = db.Column(db.String(80))
    lenddate = db.Column(db.String(80))
    returnsche = db.Column(db.String(80))
    returndate = db.Column(db.String(80))


class Lendingitem(db.Model):
    __tablename__ = "lendingitem"
    lendid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    itemname = db.Column(db.String(80))
    itemtype = db.Column(db.String(80))
    school = db.Column(db.String(80))
    lenddate = db.Column(db.String(80))
    returnsche = db.Column(db.String(80))
    returndate = db.Column(db.String(80))


# DBファイル　存在確認　なければ作成
path = "bookmnj.db"
is_file = os.path.isfile(path)
if is_file:
    print("DB:OK")
else:
    print("DBを作成します")
    db.create_all()
    db.session.commit()
    print("create DB")

if not os.path.exists("tmp"):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs("tmp")
