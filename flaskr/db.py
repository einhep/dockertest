import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
import pandas as pd
import akshare as ak

class DataFeed():
    def __init__(self):
        self.engine = self.__engine()
        # 日级数据——前复权
        self.daily_table_name_qfq = 'stock_a_daily_qfq'
        # 日级数据——后复权
        self.daily_table_name_hfq = 'stock_a_daily_hfq'

    def __engine(self):
        MYSQL_CONN_URL = "mysql+pymysql://" + os.getenv('MYSQL_USER') + ":" + os.getenv('MYSQL_PWD') + "@" \
                         + os.getenv('MYSQL_HOST') + ":3306/" + os.getenv('MYSQL_DB') + "?charset=utf8mb4"
        print(MYSQL_CONN_URL)
        engine = create_engine(MYSQL_CONN_URL, encoding='utf-8', convert_unicode=True)
        print(engine)
        return engine

    def init_db(self):
        # 获取市场所有股票代码
        print("init the db")
        stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
        codes = stock_zh_a_spot_em_df['序号'].values
        for code in codes:
            symbol_t = "%06d" % code
            print(symbol_t)
            temp_data = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="qfq")
            temp_data.to_sql(self.daily_table_name_qfq, self.engine)
            temp_data = ak.stock_zh_a_hist(symbol=symbol_t, period="daily", adjust="hfq")
            temp_data.to_sql(self.daily_table_name_hfq, self.engine)
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
