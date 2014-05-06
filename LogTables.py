#! /usr/bin/python
# -*- coding:utf-8 -*-

"""
module: table definitions
dep: sqlalchemy
"""

import string
from datetime import datetime, date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Date, Time


Base = declarative_base()

class Login(Base):
    """
    """
    __tablename__ = 'login'

    id = Column('id', Integer, primary_key = True)
    date = Column('date', Date, nullable = False)
    time = Column('time', Time, nullable = False)
    roleName = Column('role_name', String(32), nullable = False)
    ip = Column('ip', String(32), nullable = False)

    def __init__(self, dataDict):
        """
        """
        self.date = datetime.strptime(dataDict['date'], "%Y-%m-%d")
        self.time = datetime.strptime(dataDict['time'], "%H:%M:%S").time()
        self.roleName = dataDict['roleName']
        self.ip = dataDict['ip']

    def ToDict(self):
        """
        """
        dataDict = {}
        dataDict['date'] = str(self.date)
        dataDict['time'] = str(self.time)
        dataDict['roleName'] = self.roleName
        dataDict['ip'] = self.ip
        return dataDict

    def __repr__(self):
        """
        """
        return '<metadata(roleName:%s, date:%s, time:%s)' % (self.roleName, self.date, self.time)


class OnlinePlayerCount(Base):
    """
    """
    __tablename__ = 'online_player_count'

    id = Column('id', Integer, primary_key = True)
    date = Column('date', Date, nullable = False)
    clock = Column('clock', Integer, nullable = False)
    num = Column('num', Integer, nullable = False)

    def __init__(self, dataDict):
        """
        """
        self.date = datetime.strptime(dataDict['date'], "%Y-%m-%d")
        self.clock = int(dataDict['clock'])
        self.num = int(dataDict['num'])

    def ToDict(self):
        """
        """
        dataDict = {}
        dataDict['date'] = str(date)
        dataDict['clock'] = self.clock
        dataDict['num'] = self.num
        return dataDict

    def __repr__(self):
        """
        """
        return 'date: %s, clock: %d, num: %d' % (self.date, self.clock, self.num)
        

class RoleMoveInfo(Base):
    """
    """
    __tablename__ = 'role_move'
    
    id = Column('id', Integer, primary_key = True)
    date = Column('date', Date, nullable = False)
    time = Column('time', Time, nullable = False)
    roleName = Column('role_name', String(32), nullable = False)
    x = Column('x', Integer, nullable = False)
    y = Column('y', Integer, nullable = False)
    dir = Column('dir', Integer, nullable = False)
    
    def __init__(self, dataDict):
        self.date = datetime.strptime(dataDict['date'], "%Y-%m-%d")
        self.time = datetime.strptime(dataDict['time'], "%H:%M:%S").time()
        self.roleName = dataDict['roleName']
        self.x = string.atoi(dataDict['x'])
        self.y = string.atoi(dataDict['y'])
        self.dir = string.atoi(dataDict['dir'])

    def ToDict(self):
        """
        """
        dataDict = {}
        dataDict['date'] = str(date)
        dataDict['time'] = str(time)
        dataDict['roleName'] = self.roleName
        dataDict['x'] = self.x
        dataDict['y'] = self.y
        dataDict['dir'] = self.dir
        return dataDict
        
    def __repr__(self):
        return "<metadata('%s', %d, %d, %d)>" % (self.roleName, self.x, self.y, self.dir)
        
        
class ItemMoveInfo(Base):
    """
    """
    __tablename__ = 'item_move'

    id = Column('id', Integer, primary_key = True)
    date = Column('date', Date, nullable = False)
    time = Column('time', Time, nullable = False)
    type = Column('type', String(32), nullable = False)
    source = Column('source', String(32), nullable = False)
    dest = Column('dest', String(32), nullable = False)
    itemName = Column('item_name', String(32), nullable = False)
    itemCount = Column('item_count', Integer, nullable = False)
    mapId = Column('map_id', Integer, nullable = False)
    sourceIp = Column('source_ip', String(32), nullable = False)
    destIp = Column('dest_ip', String(32), nullable = False)
    
    def __init__(self, dataDict):
        self.date = datetime.strptime(dataDict['date'], "%Y-%m-%d")
        self.time = datetime.strptime(dataDict['time'], "%H:%M:%S").time()
        self.type = dataDict['type']
        self.source = dataDict['source']
        self.dest = dataDict['dest']
        self.itemName = dataDict['itemName']
        self.itemCount = string.atoi(dataDict['itemCount'])
        self.mapId = string.atoi(dataDict['mapId'])
        self.sourceIp = dataDict['sourceIp']
        self.destIp = dataDict['destIp']

    def ToDict(self):
        """
        """
        dataDict = {}
        dataDict['date'] = str(self.date)
        dataDict['time'] = str(self.time)
        dataDict['type'] = self.type
        dataDict['source'] = self.source
        dataDict['dest'] = self.dest
        dataDict['itemName'] = self.itemName
        dataDict['itemCount'] = self.itemCount
        dataDict['mapId'] = self.mapId
        dataDict['sourceIp'] = self.sourceIp
        dataDict['destIp'] = self.destIp
        return dataDict

    def __repr__(self):
        return "<metadata('%s', '%s', '%s', '%s', %d, %d, '%s', '%s')>" % (self.type, self.source, self.dest, itemName, itemCount, mapId, sourceIp, destIp)
        
        
class MonsterDie(Base):
    """
    """
    __tablename__ = 'monster_die'
    
    id = Column('id', Integer, primary_key = True)
    date = Column('date', Date, nullable = False)
    time = Column('time', Time, nullable = False)
    roleName = Column('role_name', String(32), nullable = False)
    monsterName = Column('monster_name', String(32), nullable = False)
    x = Column('x', Integer, nullable = False)
    y = Column('y', Integer, nullable = False)
    
    def __init__(self, dataDict):
        self.date = datetime.strptime(dataDict['date'], "%Y-%m-%d")
        self.time = datetime.strptime(dataDict['time'], "%H:%M:%S").time()
        self.roleName = dataDict['roleName']
        self.monsterName = dataDict['monsterName']
        self.x = string.atoi(dataDict['x'])
        self.y = string.atoi(dataDict['y'])

    def ToDict(self):
        """
        """
        dataDict = {}
        dataDict['date'] = str(self.date)
        dataDict['time'] = str(self.time)
        dataDict['roleName'] = self.roleName
        dataDict['monsterName'] = self.monsterName
        dataDict['x'] = self.x
        dataDict['y'] = self.y
        return dataDict

    def __repr__(self):
        return "<metadata('%s', '%s', %d, %d)>" % (self.roleName, self.monsterName, self.x, self.y)