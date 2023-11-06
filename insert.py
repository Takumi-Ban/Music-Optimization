import numpy as np
import csv
import sqlite3

# 接続するデータベース
db = 'music.sqlite'

# データベースを作成(すでにある場合は接続)する関数
def create_db(dbname):
    dbname = dbname
    con = sqlite3.connect(dbname)
    con.close()
    return

def dbaccess(sql, dbname, data):
    # DBを置く場所
    path = dbname

    # DBに接続
    con = sqlite3.connect(path)
    cur = con.cursor() # SQLが叩けるようになる

    # データの挿入
    if 'INSERT' in sql:
        cur.executemany(sql, data)
        con.commit()

    # データの変更を反映
    elif 'DELETE' in sql or 'UPDATE' in sql:
        cur.execute(sql)
        con.commit()

    # データの検索
    elif 'SELECT' in sql:
        cur.execute(sql)
        rows = cur.fetchall()
        con.close()
        return rows
    
    else:
        # SQLを実行する
        cur.execute(sql)

    # DBとの接続を解除
    con.close()

# CSVファイルをSQLiteに挿入可能な形式に変換する関数
def create_data(csv_path):
    data_list = []
    with open(csv_path) as f:
        reader = csv.reader(f)
        for line in reader:
            data_list.append(tuple(line))
        data_list.pop(0) # ヘッダー行の削除
    return data_list

music_info = create_data('./music_info.csv')
music_feature = create_data('./music_feature.csv')

# sql = 'INSERT INTO music_info(id, artist_name, music_name, length, release, url) VALUES (?, ?, ?, ?, ?, ?)'
# dbaccess(sql, db, music_info)

# sql = 'INSERT INTO music_feature(id, rock, pop, painful, magnificent, sad, kyomu) VALUES(?, ?, ?, ?, ?, ?, ?)'
# dbaccess(sql, db, music_feature)

sql = 'SELECT * FROM music_info'
res = dbaccess(sql, db, None)
print(res)