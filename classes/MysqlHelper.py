import mysql.connector
from json import dump


class MysqlHelper:
    client = None
    error = None

    def __init__(self, ip):
        try:
            self.client = mysql.connector.connect(
                user='root', password='', host=ip, connection_timeout=15)
        except Exception as e:
            self.error = " ".join(str(e).splitlines())

    def check(self):
        return self.error if self.error is not None else True

    def parse(self, outputFile):
        result = {}
        try:
            cursor = self.client.cursor()
            cursor.execute("SHOW DATABASES;")
            for db in [databases[0] for databases in cursor.fetchall()]:
                result[db] = {}
                cursor.execute(f"USE {db};")
                cursor.execute("SHOW TABLES;")
                for table in [tables[0] for tables in cursor.fetchall()]:
                    result[db][table] = {}
                    result[db][table]['columns'] = {}
                    cursor.execute(f"SHOW COLUMNS FROM {table}")
                    columns = cursor.fetchall()
                    for i in columns:
                        result[db][table]['columns'][i[0]] = i[1]

                    try:
                        cursor.execute(f"SELECT * FROM {table}")
                        result[db][table]['data'] = []
                        for info in cursor.fetchall():
                            temp = {}
                            for i in range(len(info)):
                                temp[columns[i][0]] = info[i]
                            result[db][table]['data'].append(temp)
                    except Exception as e:
                        result[db][table]['data'] = str(e)
        except Exception as e:
            result = " ".join(str(e).splitlines())
        dump(result, outputFile, default=str)
