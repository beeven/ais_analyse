import sqlite3
import datetime
from datetime import timezone

import os.path



def insert_into_table(filename):

    conn = sqlite3.connect("20191205.sqlite")
    with open(filename) as f:
        data = f.readlines()

    tablename = os.path.splitext(os.path.basename(filename))[0]

    cursor = conn.cursor()
    cursor.execute("""drop table if exists {0}""".format(tablename))
    cursor.execute("""create table {0} (timestamp datetime, mmsi text, latitude real, longitude real)""".format(tablename))


    for ln in data:
        fields = ln.strip().split(',')
        if fields[2] == 'None' or fields[3] == 'None' or len(fields) != 4: continue
        cursor.execute("insert into " + tablename + " values (?,?,?,?)", [datetime.datetime.fromisoformat(fields[0]), fields[1], float(fields[2]), float(fields[3])])
    
    conn.commit()
    cursor.close()
    conn.close()

def make_fact_table(mmsi):
    tablename = "compare"+mmsi
    conn = sqlite3.connect("20191205.sqlite")
    cursor = conn.cursor()
    cursor.execute("""drop table if exists """ + tablename)
    cursor.execute("create table "+tablename + "(timestamp datetime, mmsi text, latitude_dachan real, longitude_dachan real, latitude_local real, longitude_local real, latitude_fengkong real, longitude_fengkong real)")
    f = datetime.datetime(2019,12,5,1,19,0, tzinfo=timezone.utc)
    t = datetime.datetime(2019,12,5,1,35,0, tzinfo=timezone.utc)
    delta = datetime.timedelta(seconds=1)
    x = f
    while x < t:
        cursor.execute("insert into "+tablename + " values (?,?,null,null,null,null,null,null)",[x, mmsi])
        x += delta

    sql_text = """
        update compare{0}
        set mmsi = '{0}', 
            latitude_{1} = (
                select latitude from {1}20191205 
                where mmsi = '{0}' and datetime({1}20191205.timestamp) = datetime(compare{0}.timestamp)
                ),
            longitude_{1} = (
                select longitude from {1}20191205 
                where mmsi = '{0}' and datetime({1}20191205.timestamp) = datetime(compare{0}.timestamp)
                )
        where exists(
            select * from {1}20191205 
                where mmsi = '{0}' and datetime({1}20191205.timestamp) = datetime(compare{0}.timestamp)
        )
    """
    cursor.execute(sql_text.format(mmsi, 'fengkong'))
    cursor.execute(sql_text.format(mmsi, 'local'))
    cursor.execute(sql_text.format(mmsi, 'dachan'))


    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    #insert_into_table("dachan20191205.csv")
    #insert_into_table("local20191205.csv")

    make_fact_table('413494920')
