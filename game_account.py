#! /usr/bin/python
# -*- coding:utf-8 -*-
import MySQLdb
from role_sql import *
import upackZip

def Game_accountValues(role,date):

    return (role[0],date,role[1],role[2],role[3],role[4],role[5],role[6],role[7],role[8],role[9],role[10],role[11])

def import_game_account(zip_path):
    src_db_conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='yuli', db='xytx_game', charset='utf8')
    dst_db_conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='yuli', db='xytx_snapshort', charset='utf8')
    cur = src_db_conn.cursor()
    cur.execute('select count(*) from game_account')
    total = cur.fetchone()[0]
    print total
    date = upackZip.TakeTheDate(zip_path)
    size = 1000
    start = 0

    while True:
        count = cur.execute('SELECT * FROM game_account LIMIT %d, %d' % (start, size))
        roles = cur.fetchall()
        datalist =[]
        for role in roles:
            datalist.append(Game_accountValues(role,date))
            start += 1
        #print datalist
        dst_cur = dst_db_conn.cursor()
        dst_cur.executemany(sql_insert_game_account, datalist)
        dst_db_conn.commit()
        if count < size:
            break
    src_db_conn.close()
    dst_db_conn.close()
if __name__ == '__main__':
    zip_path = 'C:\\Users\\ZLove\\Desktop\\zipfiles\\20140330.zip'
    import_game_account(zip_path)
    
