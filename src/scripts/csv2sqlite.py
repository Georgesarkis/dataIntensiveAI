# Author = Amjad Alshihabi
import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
from pandas import read_sql_query
import datetime

# PATH = './Final1.csv'
# train_data = pd.DataFrame(pd.read_csv(PATH, index_col=False))

"""
    @author @name
"""
def create_table(table_name):
    conn = db_connection(table_name)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS %s (
        brand TEXT NOT NULL,
        gear TEXT NOT NULL,
        model TEXT NOT NULL,
        price INTEGER NOT NULL,
        fuel TEXT NOT NULL,
        mileage INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        type TEXT NOT NULL,
        geo TEXT NOT NULL,
        model_year INTEGER NOT NULL,
        Date TEXT NOT NULL
    );""" % table_name)
    conn.close()

"""
    @author @name
"""
def db_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)
    return conn

"""
    @author @name
"""
def insert(df, db_name):
    try:
        df = df[['brand', 'gear','model','price','fuel','mileage','hp','type','geo','model_year']]


        today=datetime.date.today()
        df['date']=today

        conn = db_connection(db_name)
        c = conn.cursor()

        data_list = df.values.tolist()
        stm="INSERT INTO cars VALUES(%s);" % ','.join('?' * 11)
        c.executemany(stm, data_list)
        conn.commit()
        conn.close()
        print('inserting is completed successfully')
    except Error as e:
        print(e)

"""
    returns all data in the given table.
    @author @name
"""
def db_read(table_name):
    try:
        conn = db_connection(table_name)
        df=pd.read_sql_query("SELECT brand ,gear ,model ,price ,fuel ,mileage ,hp ,type, geo, model_year from {}".format(table_name), conn)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    return df

"""
    @author @name
"""
def db_read_model(db_name, model):
    try:
        conn = db_connection(db_name)
        df=pd.read_sql_query("SELECT*from {} WHERE model = '{}'".format(db_name, model), conn)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    return df

"""
    returns all enteries that have been registered in the given date
    the date should be passed in the following format: datetime.datetime(yyyy, mm, dd) ex. datetime.datetime(2019, 12, 4)
    note: write months and days as: (2019, 1, 4) instead for (2019, 01, 04) otherwise the function will return an error

    @author @name
"""
def db_read_date(table_name, date:datetime.datetime):
    try:
        conn = db_connection(table_name)
        date=date.strftime('%Y-%m-%d')
        df=pd.read_sql_query("SELECT*from {} WHERE strftime('%Y-%m-%d', Date) = '{}'".format(table_name, date), conn)
        print(df.head(5))
        print('reading from database')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    return df

"""
    Returns all entries that have been registered between the two given dates.
    note: entries registered in the startDate are included and in the endDate are excluded.
    the date should be passed in the following format: datetime.datetime(yyyy, mm, dd) ex. datetime.datetime(2019, 12, 4)
    note: write months and days as: (2019, 1, 4) instead for (2019, 01, 04) otherwise the function will return an error

    to call this function you have to pass the table name,
    the start and the end dates for the period which the data has been inserted to the db,
    
    @author @name
"""
def db_read_period(table_name, startDate:datetime.datetime, endDate:datetime.datetime):
    if startDate>endDate:
        print('start date cannot be less than end date')
        return False
    try:
        conn = db_connection(table_name)
        startDate=startDate.strftime('%Y-%m-%d')
        endDate=endDate.strftime('%Y-%m-%d')
        print('reading from database')
        df=pd.read_sql_query("SELECT*from {} WHERE strftime('%Y-%m-%d', Date) >= '{}' AND strftime('%Y-%m-%d', Date) < '{}'".format(table_name, startDate, endDate), conn)
        print(df.head(5))
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    return df

# create_table('cars')
# insert(train_data, 'cars')
# df=db_read_period('cars', datetime.datetime(2019, 12, 8), datetime.datetime(2019, 12, 10))
