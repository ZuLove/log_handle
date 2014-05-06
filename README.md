1、安装本程序依赖的第三方python插件
（1）、安装本目录下的pycrypto-2.6.win32-py2.7.exe文件
（2）、再解压本目录下的paramiko-1.13.0.tar.gz文件，并安如下步凑安装：
      1、 cd paramiko-1.13.0
      2、 python setup.py build
      3、 python setup.py install
不同电脑可能有所区别，具体可网上搜索安装过程

2、修改文件logTables.py

create database if not exists xytx_qiyuan;
use xytx_qiyuan;
将文件logTables.py中上面两句中的xytx_qiyuan修改为相应的日志数据库的名字，
格式为‘xytx_区名’，然后执行该sql语句，如果多个区，可修改并执行该sql

3、执行本目录下的xytx_snapshort.sql文件

4、修改down_from_server_ini.py文件
（1）、服务器配置信息
（2）、本地zip存放目录
（3）、远程服务器zip存放目录
5、运行本目录下的main.py文件，然后耐心等带个把小时就ok