# 備品/書籍貸出システム
## 概要
バンタン名古屋校の備品管理システム.
書籍,備品の貸出記録をDBに記録する。

## 動作環境
Python3.9
Flask 2.2.2
DB:sqlite3 or mysql

## 開発環境構築
pipenvを使用してPipfileから必須モジュールをインストールして下さい。

## init
以下のコードを実行して、tmpフォルダ,データベースを作成してください。
```bash
python init.py
```

## 使い方
```bash
FLASK_APP=main.py flask run
```

## データベース設計
### 備品テーブル
|カラム名|型|説明|
|:--|:--|:--|
|lendid|integer|備品貸出記録に対しての固有のID(pk)|
|name|string|貸出者の名前|
|itemname|string|備品の名前|
|itemtype|string|備品を所有しているスクール名|
|school|string|貸出者の所属スクール|
|lenddate|string|貸出日|
|returnsche|string|返却予定日|
|returndate|string|返却日 未返却の場合NULL|

### 書籍テーブル
|カラム名|型|説明|
|:--|:--|:--|
|lendid|integer|書籍貸出記録に対しての固有のID(pk)|
|name|string|貸出者の名前|
|bookname|string|書籍の名前|
|school|string|貸出者の所属スクール|
|lenddate|string|貸出日|
|returnsche|string|返却予定日|
|returndate|string|返却日 未返却の場合NULL|


## データベース接続設定
main.pyの
```
app.config["SQLALCHEMY_DATABASE_URI"] = {uri}
```
を編集してください。

## 使用した技術
templateエンジン:jinja2
CSSフレームワーク:Bootstrap4
Webアプリケーションフレームワーク:Flask 2.2.2
ORM:SQLAlchemy

## Todo
・UI/UX改善
