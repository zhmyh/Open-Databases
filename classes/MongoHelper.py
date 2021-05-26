from pymongo import MongoClient
from json import dumps, load

class MongoHelper:
    def __init__(self, ip, port=27017):
        try:
            self.client = MongoClient(ip, port, serverSelectionTimeoutMS = 30000)
        except:
            pass

    def check(self):
        try:
            self.client.list_database_names()
            return True
        except Exception as e:
            return " ".join(str(e).splitlines())

    def parse(self, outputFile):
        try:
            for db in self.client.list_database_names():
                outputFile.write('Database %s\n\n' % (db))
                for collection in self.client[db].list_collection_names():
                    outputFile.write('Collection %s\n\n' % (collection))
                    for document in self.client[db][collection].find():
                        outputFile.write(dumps(document, indent=2, default=str))
                        outputFile.write('\n')
        except Exception as e:
            outputFile.write(" ".join(str(e).splitlines()))
