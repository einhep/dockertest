import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import akshare as ak
import time

# base class of table object
Base = declarative_base()

#
# class DataDailyQFQ(Base):
#     # name of the table
#     __tablename__ = 'stock_a_daily_qfq'
#     # struct of the table
#     id = Column(string)
    
class DataBase():
    def __init__(self):
        # connector_str
        self._mysql_conn_url = "mysql+pymysql://" + os.getenv('MYSQL_USER') + ":" + os.getenv('MYSQL_PWD') + "@" \
                         + os.getenv('MYSQL_HOST') + ":3306/" + os.getenv('MYSQL_DB') + "?charset=utf8mb4"
        #
        self.engine = create_engine(self._mysql_conn_url, encoding='utf-8', convert_unicode=True)
        # create database
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        # 日级数据——前复权
        self.daily_table_name_qfq = 'stock_a_daily_qfq'
        # 日级数据——后复权
        self.daily_table_name_hfq = 'stock_a_daily_hfq'

    def init_db(self):
        # 获取市场所有股票代码
        print("init the db")
        # step 1: 检查是否存在数据库，如果不存在则创建

        # step 2: get the history data
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
        codes = stock_zh_a_spot_em_df['代码'].values
        print("total having %d company" % len(codes))
        for count, code in enumerate(codes):
            print("processing %s in %d/%d (count+1 / total)" % (code, count+1, len(codes)))
            import math
            if math.isnan(stock_zh_a_spot_em_df['最新价'].values[count]):
                print("processing done with Nan")
                continue
            print("processing done with normal")
            symbol_t = code
            try:
                temp_data_qfq = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="qfq")
                temp_data_hfq = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="hfq")
            except:
                time.sleep(30.1)
                try:
                    temp_data_qfq = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="qfq")
                    temp_data_hfq = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="hfq")
                except:
                    return "processing %s in %d/%d (count+1 / total)" % (code, count+1, len(codes))
            temp_data_qfq.loc[:, '代码'] = code
            temp_data_qfq.to_sql(self.daily_table_name_qfq, self.engine, if_exists='append', index=False)
            temp_data_hfq.loc[:, '代码'] = code
            temp_data_hfq.to_sql(self.daily_table_name_hfq, self.engine, if_exists='append', index=False)
        return "sss"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == "__main__":
    db = DataBase()
    db.init_db()