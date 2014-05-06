#! /usr/bin/python
# -*- coding:utf-8 -*-

import json,os,re
import string
import ctypes
import MySQLdb
from role_sql import *
import upackZip,game_account
global libBinToJson
from down_from_server import *
from down_from_server_ini import *

def RoleValues(date,role):
    """
    """
    return (
        date, role['roleName'], role['roleName'], role['roleName'], role['payType'], role['accountName'],
        role['itemsPassword'], role['groupKey'],  role['guild'], role['lastDate'], role['createDate'],
        role['sex'], role['x'], role['y'], role['goldLngot'], role['light'], role['dark'], role['inPower'],
        role['outPower'], role['life'], role['adaptive'], role['revival'], role['immunity'], role['virtue'],
        role['curInPower'], role['curOutPower'], role['curLife'], role['curHealth'], role['curSatiety'],
        role['curPoisoning'], role['curHeadSeek'], role['curArmSeek'], role['curLegSeek']
    )


def ItemValues(owner, index, item, date):
    """
    """
    if item['rDateTime'] == '':
        item['rDateTime'] = date

    return (
        date, owner, index,item['rID'],item['rName'],item['rCount'], item['rColor'], item['rDurability'],
        item['rDurabilityMAX'], item['rSmithingLevel'], item['rAttach'], item['rlockState'], item['rlocktime'],
        item['rDateTime'], item['rBoident'], item['rStarLevel'], item['rboBlueprint'], item['rSpecialExp'],
        item['rCreateName'], item['rDummy1'], item['rDummy2'], item['rDummy3'], item['rDummy4'],
        item['rSetting']['rsetting1'], item['rSetting']['rsetting2'],
        item['rSetting']['rsetting3'], item['rSetting']['rsetting4']
    )


def MagicValues(owner, index, magic,date):
    """
    """
    return (date, owner, index, magic['name'], magic['exp'])

def ConvertRole(rolename, data,libBinToJson,date,dst_db_conn):
    """
    """
    data = ctypes.c_char_p(data)
    data = ctypes.c_char_p(libBinToJson.binToJson(data.value)).value
    try:
        data = json.loads(data.decode('gb2312'))
    except Exception as e:
        print data

    cur = dst_db_conn.cursor()
    cur.executemany(sql_insert_role, (RoleValues(date,data),))
    params = []
    for k, v in sorted(data['equipments'].items(), key = lambda e:string.atoi(e[0])):
        if v['rName'] != '':
            params.append(ItemValues(rolename, k, v, date))
    cur.executemany(sql_insert_wear_item, params)

    params = []
    for k, v in sorted(data['backpacks'].items(), key = lambda e:string.atoi(e[0])):
        if v['rName'] != '':
            params.append(ItemValues(rolename, k, v, date))
    cur.executemany(sql_insert_bag_item, params)
    
    params = []
    for k, v in sorted(data['baseMagics'].items(), key = lambda e:string.atoi(e[0])):
        if v['name'] != '':
            params.append(MagicValues(rolename, k, v,date))
    cur.executemany(sql_insert_base_magic, params)

    params = []
    for k, v in sorted(data['advMagics'].items(), key = lambda e:string.atoi(e[0])):
        if v['name'] != '':
            params.append(MagicValues(rolename, k, v, date))
    cur.executemany(sql_insert_advanced_magic, params)

    dst_db_conn.commit()


def main(zip_path):
    
    libBinToJson = ctypes.windll.LoadLibrary('./binToJson.dll')
    date = upackZip.TakeTheDate(zip_path)
    src_db_conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='yuli', db='xytx_game', charset='utf8')
    dst_db_conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='yuli', db='xytx_snapshort', charset='utf8')
    cur = src_db_conn.cursor()
    cur.execute('SELECT COUNT(*) FROM role')
    total = cur.fetchone()[0]

    #date = '2014-3-12'
    size = 1000
    start = 0

    while True:
        count = cur.execute('SELECT role_name, role_info FROM role LIMIT %d, %d' % (start, size))
        roles = cur.fetchall()
        for role in roles:
            ConvertRole(role[0], role[1],libBinToJson,date,dst_db_conn)
            start += 1

        if count < size:
            break
    src_db_conn.close()
    dst_db_conn.close()
    
if __name__ == '__main__':
    """
    """
    #ssh_linux_to_win(local_dir,remote_dir)
    files = os.listdir(local_dir)
    if files ==[]:
        print '没有文件文件'
    else:
        import time
        s = time.time()
        for filex in files:
            if os.path.splitext(filex)[-1] == '.zip':
                match = re.search('_',filex)
                print 'xytx_'+filex[:match.start()]
                database_name = 'xytx_'+filex[:match.start()]
                zip_path = os.path.join(local_dir,filex)
                print zip_path
                print u'开始解压...'
                upackZip.UpackZip(zip_path)
                print u'解压完毕'
                print u'开始导入xytx_game数据库...'
                upackZip.ExecuteSql(zip_path)
                print u'导入完毕'
                print u'开始将xytx_game数据库的game_account数据导入xytx_snapshort的game_account...'
                #game_account.import_game_account(zip_path)
                print u'导入完毕'
                print u'开始将日志文件转为CSV文件...'
                upackZip.ChangeLogToCSV(zip_path)
                print u'转化完毕'
                print u'开始将CSV文件导入log-database数据库...'
                upackZip.findCSV(zip_path)
                #upackZip.CSVToDatabase(database_name)
                print u'导入完毕'
                #main(zip_path)

        print 'Total:',time.time()-s
    
       
