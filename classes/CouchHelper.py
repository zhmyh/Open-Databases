import couchdb

class CouchHelper:
    def __init__(self, ip, port=5984):
        try:
            self.client = couchdb.Server("http://%s:%s/" % (ip, port))
        except:
            pass

    def check(self):
        try:
            self.client.tasks()
            return True
        except Exception as e:
            return " ".join(str(e).splitlines())

    # def parse(self, outputFile):
    #     if self.client:
    #         for dbname in self.client:
    #             for docid in self.client[dbname].view('_all_docs'):
    #                 print(docid)
