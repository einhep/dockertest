# !/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "mysqldb"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "mysqldb"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

print("MYSQL_HOST :", MYSQL_HOST, ",MYSQL_USER :", MYSQL_USER, ",MYSQL_DB :", MYSQL_DB)
MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB + "?charset=utf8mb4"
print("MYSQL_CONN_URL :", MYSQL_CONN_URL)

class Persister(object):
    def __init__(self):
        self.DbSession = None
        self.isClose = True
        self.session = None

    def open(self,host=configuration.host,port=configuration.port,db=configuration.db,user=configuration.user,pwd=configuration.pwd) :

        url = 'mysql+mysqlconnector://%s:%s@%s:%d/%s' % (user,pwd,host,port,db)
        engine = create_engine(url)
        DbSession = sessionmaker(bind=engine)

        self.session = DbSession()

        self.isClosed = False

        return self.session

    def query(self,type):
        query = self.session.query(type)
        return query

    def add(self,item):
        self.session.add(item)

    def add_all(self,items):
        self.session.add_all(items)

    def delete(self,item):
        self.session.delete(item)

    def commit(self):
        self.session.commit()

    def close(self):

        if self.isClosed:
            pass

        self.session.close()
        self.isClosed = True

if __name__= '__main__':
