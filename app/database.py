#!/usr/bin/env python

from java.lang import Class
from java.sql  import DriverManager, SQLException

TABLE_DROPPER = "drop table if exists entries;"
TABLE_CREATOR = """
create table entries(
	id integer primary key autoincrement,
	title text not null,
	text text not null
);
"""

def connect_db(jdbc_url, driverName):
    try:
        Class.forName(driverName).newInstance()
        dbConn = DriverManager.getConnection(jdbc_url)
    except Exception, msg:
        print msg
        sys.exit(1)

    return dbConn

def init_db(jdbc_url, driveName):
    db = connect_db(jdbc_url, driveName)
    stmt = db.createStatement()
    try:
        stmt.executeUpdate(TABLE_DROPPER)
        stmt.executeUpdate(TABLE_CREATOR)
    except SQLException, msg:
        print msg
        sys.exit(1)
    stmt.close()
    db.close()

