import psycopg2
import json

class PostgreHelper:
    client = None
    error = None

    def __init__(self, ip):
        try:
            self.client = psycopg2.connect(connect_timeout=30, dbname='postgres', user='postgres', host=ip, password='postgres')
        except Exception as e:
            self.error = "".join(str(e).splitlines())


    def check(self):
        return self.error if self.error is not None else True

    def parse(self, outputFile):
        result = {}
        db_cursor = self.client.cursor()
        sql = "SELECT table_schema, table_name FROM information_schema.tables"
        db_cursor.execute(sql)
        list_tables = db_cursor.fetchall()
        for table in list_tables:
            try:
                if table[0] not in result:
                    result[table[0]] = {}
                tempResult = {}

                sql = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table[1]}'"
                db_cursor.execute(sql)
                table_columns = db_cursor.fetchall()

                tempResult["columns"] = {}
                for i in table_columns:
                    tempResult["columns"][i[0]] = i[1]


                sql = f"SELECT * FROM {table[0]}.{table[1]}"
                db_cursor.execute(sql)
                table_info = db_cursor.fetchall()

                tempResult["data"] = []
                for info in table_info:
                    temp = {}
                    for i in range(len(info)):
                        temp[table_columns[i][0]] = info[i]
                    tempResult["data"].append(temp)
                result[table[0]][table[1]] = tempResult
            except Exception as e:
                result[table[0]][table[1]] = " ".join(str(e).splitlines())

        json.dump(result, outputFile, default=str)
