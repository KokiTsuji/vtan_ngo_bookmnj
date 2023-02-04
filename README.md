# 備品/書籍貸出システム
## 概要
バンタン名古屋校の備品管理システム.

## 動作環境
Python3.9が動作する環境

## 開発環境構築
venvを使用してPipfileから必須モジュールをインストールして下さい。

## 使い方
データベースを配置して起動してください。
```bash
python main.py
```
データベースを作成した後はmain.pyを実行してください。

## データベース設定
main.pyのapp.config行を編集してください。

## 仕様
templateエンジン:jinja2
CSSフレームワーク:Bootstrap4

## Todo
・UI/UX改善