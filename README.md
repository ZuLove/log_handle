1����װ�����������ĵ�����python���
��1������װ��Ŀ¼�µ�pycrypto-2.6.win32-py2.7.exe�ļ�
��2�����ٽ�ѹ��Ŀ¼�µ�paramiko-1.13.0.tar.gz�ļ����������²��հ�װ��
      1�� cd paramiko-1.13.0
      2�� python setup.py build
      3�� python setup.py install
��ͬ���Կ����������𣬾��������������װ����

2���޸��ļ�logTables.py

create database if not exists xytx_qiyuan;
use xytx_qiyuan;
���ļ�logTables.py�����������е�xytx_qiyuan�޸�Ϊ��Ӧ����־���ݿ�����֣�
��ʽΪ��xytx_��������Ȼ��ִ�и�sql��䣬�������������޸Ĳ�ִ�и�sql

3��ִ�б�Ŀ¼�µ�xytx_snapshort.sql�ļ�

4���޸�down_from_server_ini.py�ļ�
��1����������������Ϣ
��2��������zip���Ŀ¼
��3����Զ�̷�����zip���Ŀ¼
5�����б�Ŀ¼�µ�main.py�ļ���Ȼ�����ĵȴ�����Сʱ��ok