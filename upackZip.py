#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
made by ZLove
"""
import zipfile
import os
import csv
import logging

def UpackZip(zip_path):
     #设置解压文件夹路径
    extract_path = os.path.splitext(zip_path)[0]
    print extract_path
    #取得Zip文件对象
    file_zip = zipfile.ZipFile(zip_path, 'r')
    #解压文件到指定文件夹下
    file_zip.extractall(extract_path)
    file_zip.close()
            
def TakeTheDate(zip_path):
    zipdir_path = os.path.splitext(zip_path)[0]
    file_list = os.listdir(zipdir_path)
    for file_name in file_list:
        #根据文件夹名找到相应的文件夹
        #print file_name
        if os.path.splitext(file_name)[-1] == '.sql':
            #path = os.path.join(zipdir_path, os.path.splitext(file_name)[0])
            #获取相应文件夹下的所有文件
            sql_name = os.path.splitext(file_name)[0]
            #获取sql文件名中的相应日期
            date = sql_name[-8:-4]+'-'+sql_name[-4:-2]+'-'+sql_name[-2:]
            #print date
            return date
        
            
def ExecuteSql(zip_path):
    zipdir_path = os.path.splitext(zip_path)[0]
    file_list = os.listdir(zipdir_path)
    #获取sql文件所在文件夹路径
    for file_name in file_list:
        if os.path.splitext(file_name)[-1] == '.sql':
            #获取sql文件所在绝对路径
            sql_path = zipdir_path + os.path.join('\\',file_name)
            print sql_path
            cmdStr ='mysql -uroot -pyuli -Dxytx_game< %s' %(sql_path,)
            #执行sql文件
            os.system(cmdStr)

def CSVToDatabase(database_name):
    sql_path = './CSVToDatabase.sql'
    cmdStr ='mysql -uroot -pyuli -D%s< %s' %(database_name,sql_path)
    print cmdStr
    os.system(cmdStr)
    
def WriteCSV(file_abspath,csvfile_name):
    file_obj = open(file_abspath,'r')
    csvfile = open(csvfile_name, 'a')
    #log_name = os.path.splitext(csvfile_name)[0]+'.log'
    #logger = logging.getLogger('csvlog')  
    #logger.setLevel(logging.DEBUG)  
    #fh = logging.FileHandler(log_name)
    #fh.setLevel(logging.DEBUG)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh.setFormatter(formatter)
    #logger.addHandler(fh)
    writer = csv.writer(csvfile)
    dataxlist =[]
    for filelog in file_obj:
        datalist = []
        filelog = filelog.strip('\n').split(',')
        #rint filelog
        for datastr in filelog:
            index = datastr.find(':')
            data = datastr[index+1:]
            datalist.append(data.decode('gbk').encode('utf8'))
        dataxlist.append(datalist)
        if len(dataxlist)==1000:
            writer.writerows(dataxlist)
            dataxlist =[]
    writer.writerows(dataxlist)
        #writer.writerow(datalist)
        #logger.info(datalist)
    csvfile.close()
    file_obj.close()
        
def ChangeLogToCSV(zip_path):
    rootDir = os.path.splitext(zip_path)[0]
    file_list = os.listdir(rootDir)
    for dir_name in file_list:
        if os.path.splitext(dir_name)[1] == '':
            log_file_path = rootDir + '\\' + dir_name
            list_dirs = os.walk(log_file_path)
            for root, dirs, files in list_dirs:
                for f in files:
                    if f[-4:]== '.log':
                        file_abspath = os.path.join(root, f)
                        if dirs:
                            file_name = f[:-4]
                            csvfile_name = rootDir+'\\'+file_name +'.csv'
                            WriteCSV(file_abspath,csvfile_name)
                        else:
                            file_name = file_abspath.split('\\')[-2]
                            print file_name
                            csvfile_name = rootDir+'\\'+file_name +'.csv'
                            print csvfile_name
                            WriteCSV(file_abspath,csvfile_name)
def findCSV(zip_path): 
    extract_path = os.path.splitext(zip_path)[0]
    with open('./CSVToDatabase.sql','w') as file_obj:
        
        for file_s in os.listdir(extract_path):
            csv_path = extract_path +os.sep + file_s
            csv_path = csv_path.replace('\\','\\\\')
            if file_s[:-4] == 'monsterDie':
                cmdStr = 'load data infile ' + '\''+csv_path +'\''+ r" into table monster_die fields terminated by ',' optionally enclosed by " + "'\"' escaped by '\"'" + r" lines terminated by '\r\n' (date,time,role_name,monster_name,x,y);"
                file_obj.writelines(cmdStr+'\n')
            elif file_s[:-4] =='login':
                cmdStr = 'load data infile '+ '\''+csv_path +'\''+ r" into table login fields terminated by ',' optionally enclosed by "+ "'\"' escaped by '\"'" + r" lines terminated by '\r\n' (date,time,role_name,ip);"
                file_obj.writelines(cmdStr+'\n')
            elif file_s[:-4] =='OnlinePlayerCount':
                cmdStr = 'load data infile '+ '\''+csv_path +'\''+ r" into table online_player_count fields terminated by ',' optionally enclosed by " + "'\"' escaped by '\"'" + r" lines terminated by '\r\n' (date,time,clock,num);"
                file_obj.writelines(cmdStr+'\n')
            elif file_s[:-4] =='item':
                cmdStr = str4 = 'load data infile '+ '\''+csv_path +'\''+ r" into table item_move fields terminated by ',' optionally enclosed by "+ "'\"' escaped by '\"'" + r" lines terminated by '\r\n' (date,time,type,source,dest,item_name,item_count,map_id,x,y,source_ip,dest_ip);"
                file_obj.writelines(cmdStr+'\n')
    
if __name__ == '__main__':
    file_name = '20140330'
    #zipdir_path = 'C:\Users\ZLove\Desktop\zipfiles'
    zip_path = 'C:\\Users\\ZLove\\Desktop\\zipfiles\\qiyuan_bak_2014_04_18_09_30_01'
    #print zipdir_path1
##    zipdir_path2 = zip_path.split('\\')
##    zipdir_path3 = os.path.splitext(zip_path)[0].split('\\')
##    print zipdir_path3
##    file_name = zipdir_path2[-1]
##    print zipdir_path2
##    print file_name
    #UpackZip(zip_path)
    #TakeTheDate(file_name,zipdir_path)
##    ExecuteSql(zipdir_path)
    #rootpath = zipdir_path +'\\'+ file_name
    #print rootpath
    import time
    s=time.time()
    ChangeLogToCSV(zip_path)
    print 'Total:',time.time()-s
    #tablename = 'game_account'
    #DumpTable(tablename,rootpath)
    
