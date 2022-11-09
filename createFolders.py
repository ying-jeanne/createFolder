import sqlite3
from sqlite3 import Error
from datetime import datetime
import random
import string  

def lower_string(length): # define the function and pass the length as argument  
    # generate the string in Lowercase  
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length  
    return result 


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_folder(conn, folder):
    """
    Create a new folder into the folder table
    :param uid:
    :param org_id:
    :param title
    :param description
    :param parent_uid
    :param created
    :param updated
    :return: project id
    """
    sql = ''' INSERT INTO folder(uid,org_id,title,parent_uid,created,updated)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, folder)
    conn.commit()
    return cur.lastrowid

def generateChildren(conn, parent_uid, dept, treeWidth, parentId):
    if dept == 0: return
    dept = dept - 1
    for i in range(1, treeWidth):
        newparentId = parentId + '.' + str(i)
        uid =  parentId +lower_string(5)
        title = lower_string(10)
        f = (uid, 1, title, parent_uid, datetime.now(), datetime.now());
        create_folder(conn, f)
        generateChildren(conn, uid, dept, treeWidth, newparentId)

def main():
    dept = 4
    treeWidth = 3
    database = "/Users/ying-jeanne/Workspace/grafana/data/grafana.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        generateChildren(conn, 'general', dept-1, treeWidth, '1')


if __name__ == '__main__':
    main()