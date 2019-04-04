import pymysql

class SqlRW(object):
    def __init__(self, host, port, user, password, database, c_timeout=30):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn_timeout = c_timeout

    def __GetConnect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database, charset='utf8', cursorclass=pymysql.cursors.DictCursor,
                                    connect_timeout=self.conn_timeout)
        cursor = self.conn.cursor()
        if not cursor:
            print('connected failed')
        return cursor

    def ReadSql(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.close()
        return result

    def WriteSql(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        return 1
