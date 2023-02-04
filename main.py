
from flask import Flask, render_template, request, redirect, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import and_
import os
import datetime
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmnj.db"  # データベースの場所を指定
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)  # データベースに接続

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


# # DBファイル　存在確認
# path = "bookmnj.db"
# is_file = os.path.isfile(path)
# if is_file:
#     print("DBConnection OK")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/lending") #書籍の貸出ページ
def lending():
    date = datetime.datetime.now().date()  # 今日の日付を代入
    d_7d = date + datetime.timedelta(days=7)  # 7日後の日付を代入
    return render_template("lend.html", date=date, d_7d=d_7d)


@app.route("/lending-item") #備品の貸出ページ
def lending_item():
    date = datetime.datetime.now().date()  # 今日の日付を代入
    d_1d = date + datetime.timedelta(days=1) #1日後の日付を代入
    return render_template("lend-item.html")


@app.route("/oklending", methods=["POST"]) #書籍の貸出処理
def oklending():
    name = request.form.get("name_sei").strip() + " " + request.form.get("name_mei").strip()
    bookname = request.form.get("bookname")
    school = request.form.get("school")
    lendsche = request.form.get("returnsche_date")
    lenddate = str(datetime.date.today())

    lend = Lending(
        name=name,
        school=school,
        bookname=bookname,
        lenddate=lenddate,
        returnsche=lendsche,
    )
    db.session.add(lend)
    db.session.commit()
    flash("書籍を貸出しました", "success")
    return redirect("/")


@app.route("/oklending-item", methods=["POST"]) #備品の貸出処理
def oklendingitem():
    name = request.form.get("name_sei").strip() + " " + request.form.get("name_mei").strip()
    itemname = request.form.get("bookname")
    itemtype = request.form.get("itemtype")
    school = request.form.get("school")
    lendsche = datetime.date.today()
    lenddate = str(datetime.date.today())
    lend = Lendingitem(
        name=name,
        school=school,
        itemname=itemname,
        itemtype=itemtype,
        lenddate=lenddate,
        returnsche=lendsche,
    )
    db.session.add(lend)
    db.session.commit()
    flash("備品を貸出しました", "success")
    return redirect("/")

@app.route("/listlending")
def listlending():
    filters = [] # 検索条件を格納するタプル
    if request.args.get("name_sei") or request.args.get("name_mei"):
        name = str(request.args.get("name_sei")) + " " + str(request.args.get("name_mei"))
    else:
        name = ""
    req = request.args.get("onlyunreturned")
    startdate = request.args.get("startdate")
    enddate = request.args.get("enddate")

    if name:
        filters.append(Lending.name.like("%" + name + "%"))
    if startdate and enddate:
        filters.append(and_(Lending.lenddate >= startdate, Lending.lenddate <= enddate))
    if req == "yes":
        filters.append(Lending.returndate == None)

    lendings = db.session.query(
        Lending.lendid,
        Lending.name,
        Lending.school,
        Lending.bookname,
        Lending.lenddate,
        Lending.returnsche,
        Lending.returndate,
    ).filter(and_(*filters)
    ).all()  # 履歴を取得

    lendings.reverse()  # 新しい順に並び替える

    page = request.args.get(get_page_parameter(), type=int, default=1) # ページ番号を取得
    rows = lendings[(page - 1)*50: page*50] # n件ずつ表示
    pagination = Pagination(page=page, total=len(lendings), display_msg='<b>{total}</b> {record_name}中の <b>{start} - {end}</b> {record_name}', record_name='件', per_page=50, css_framework='bootstrap4') #ページネーション

    return render_template("listlending.html", pagination=pagination, rows=rows)

@app.route("/listlending-item")
def listlending_bihin():
    filters = [] # 検索条件を格納するタプル
    if request.args.get("name_sei") or request.args.get("name_mei"):
        name = str(request.args.get("name_sei")) + " " + str(request.args.get("name_mei"))
    else:
        name = ""
    req = request.args.get("onlyunreturned")
    startdate = request.args.get("startdate")
    enddate = request.args.get("enddate")
    # itemtype = request.args.get("itemtype")

    if name:
        filters.append(Lendingitem.name.like("%" + name + "%"))
    if startdate and enddate:
        filters.append(and_(Lendingitem.lenddate >= startdate, Lendingitem.lenddate <= enddate))
    if req == "yes":
        filters.append(Lendingitem.returndate == None)

    lendings = db.session.query(
        Lendingitem.lendid,
        Lendingitem.name,
        Lendingitem.school,
        Lendingitem.itemname,
        Lendingitem.itemtype,
        Lendingitem.lenddate,
        Lendingitem.returnsche,
        Lendingitem.returndate,
    ).filter(and_(*filters)
    ).all()  # 履歴を取得

    lendings.reverse()  # 新しい順に並び替える

    page = request.args.get(get_page_parameter(), type=int, default=1) # ページ番号を取得
    rows = lendings[(page - 1)*50: page*50] # n件ずつ表示
    pagination = Pagination(page=page, total=len(lendings), display_msg='<b>{total}</b> {record_name}中の <b>{start} - {end}</b> {record_name}', record_name='件', per_page=50, css_framework='bootstrap4') #ページネーション

    return render_template("listlending-item.html", pagination=pagination, rows=rows)


@app.route("/admin/returnd", methods=["GET", "POST"])
#@login_required
def okreturnd():
    if request.method == "POST":
        lendid = request.form.get("lendid")
        dt_now = datetime.datetime.now()
        returndate = (
            str(dt_now.year) + "-" + str(dt_now.strftime("%m")) + "-" + str(dt_now.strftime("%d"))
        )  # 返却日を現在の日付にする
        lendingbook = (
            db.session.query(Lending)
            .filter(and_(Lending.lendid == lendid, Lending.returndate == None))
            .first()
        )  # 未返却でlendidが一致する一つ目ものを取得
        lendingbook.returndate = returndate
        db.session.commit()
        flash("書籍を返却しました", "success")
        return redirect("/listlending")
    else:
        req = request.args.get("lendid")
        if req == None:
            pass
        else:
            lendrow = (
                db.session.query(
                    Lending.lendid,
                    Lending.name,
                    Lending.school,
                    Lending.bookname,
                    Lending.lenddate,
                    Lending.returnsche,
                )
                .filter(Lending.lendid == req)
                .first()
            )  # lendidが一致する一つ目ものを取得
        return render_template("returnd.html", lendlist=lendrow)


@app.route("/admin/returnd-item", methods=["GET", "POST"])
#@login_required
def okreturnd_item():
    if request.method == "POST":
        lendid = request.form.get("lendid")
        dt_now = datetime.datetime.now()
        returndate = (
            str(dt_now.year) + "-" + str(dt_now.strftime("%m")) + "-" + str(dt_now.strftime("%d"))
        )  # 返却日を現在の日付にする
        lendingbook = (
            db.session.query(Lendingitem)
            .filter(and_(Lendingitem.lendid == lendid, Lendingitem.returndate == None))
            .first()
        )  # 未返却でlendidが一致する一つ目ものを取得
        lendingbook.returndate = returndate
        db.session.commit()
        flash("備品を返却しました", "success")
        return redirect("/listlending-item")
    else:
        req = request.args.get("lendid")
        if req == None:
            pass
        else:
            lendrow = (
                db.session.query(
                    Lendingitem.lendid,
                    Lendingitem.name,
                    Lendingitem.school,
                    Lendingitem.itemname,
                    Lendingitem.itemtype,
                    Lendingitem.lenddate,
                    Lendingitem.returnsche,
                )
                .filter(Lendingitem.lendid == req)
                .first()
            )  # lendidが一致する一つ目ものを取得
        return render_template("returnd-item.html", lendlist=lendrow)


@app.route("/writecsv", methods=["GET", "POST"])
def writecsv():
    if request.method == "POST":
        itemtype = request.form.get("itemtype")
        if itemtype == "item":
            lenddate = db.session.query(
                Lendingitem.name,
                Lendingitem.school,
                Lendingitem.itemname,
                Lendingitem.itemtype,
                Lendingitem.lenddate,
                Lendingitem.returnsche,
                Lendingitem.returndate,
            ).all()
            lendpoint = [
                "名前",
                "所属スクール",
                "備品名",
                "備品種別",
                "貸出日",
                "返却予定日",
                "返却状況",
            ]  # ヘッダ行設定
        elif itemtype == "book":
            lenddate = db.session.query(
                Lending.name,
                Lending.school,
                Lending.bookname,
                Lending.lenddate,
                Lending.returnsche,
                Lending.returndate,
            ).all()
            lendpoint = ["名前", "所属スクール", "書籍名", "貸出日", "返却予定日", "返却状況"]  # ヘッダ行設定
        sort_reverse = request.form.get("reverse")
        if sort_reverse == "yes":
            lenddate.reverse()  # 新しい順に並び替える
        f = open(f"tmp/{itemtype}list.csv", "w", newline="", encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(lendpoint)  # CSVのヘッダ行を書き込み
        writer.writerows(lenddate)  # CSVのデータ行を書き込み
        f.close()

        # ダウンロード処理
        minetype = "text/csv"
        dlfile = f"tmp/{itemtype}list.csv"
        return send_file(
            dlfile,
            mimetype=minetype,
            as_attachment=True,
            download_name=f"{itemtype}list.csv",
        )
    else:
        return render_template("writecsv.html")


## おまじない
if __name__ == "__main__":
    app.run(debug=True)
