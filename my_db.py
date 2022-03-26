import sqlite3
import traceback
import sys

class DB:
    def create_table(self):
        con = sqlite3.connect(r'my.db', isolation_level = None)
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS User_Info(id INTEGER PRIMARY KEY, pos TEXT, w INTEGER DEFAULT 0, l INTEGER DEFAULT 0)")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        con.close()
    def regist(self, id:int, pos:str) -> bool:
        con = sqlite3.connect(r'my.db', isolation_level = None)
        cur = con.cursor()
        try:
            cur.execute("INSERT OR REPLACE INTO User_Info(id,pos) VALUES({}, \'{}\')".format(id,pos))
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        con.close()
        return True, "등록, 수정 완료"
    def get(self, id:int):
        con = sqlite3.connect(r'my.db', isolation_level = None)
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM User_Info WHERE id = '{}'".format(id))
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

        record = cur.fetchone()
        con.close()

        if record == None:
            return False, "등록되지 않은 사용자입니다."

        return True, record
    def set_win(self, id:int):
        con = sqlite3.connect(r'my.db', isolation_level = None)
        cur = con.cursor()

        try:
            cur.execute("UPDATE User_Info SET w = w + 1 WHERE id = '{}'".format(id))
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        con.close()
    def set_lose(self, id:int):
        con = sqlite3.connect(r'my.db', isolation_level = None)
        cur = con.cursor()

        try:
            cur.execute("UPDATE User_Info SET l = l + 1 WHERE id = '{}'".format(id))
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        con.close()
