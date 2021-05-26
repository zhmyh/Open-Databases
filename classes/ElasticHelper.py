from elasticsearch import Elasticsearch
from json import dumps


class ElasticHelper:
    def __init__(self, ip, port=9200):
        self.client = Elasticsearch([{'host': ip, 'port': 9200}])

    def check(self):
        try:
            self.client.ping()
            return True
        except Exception as e:
            return " ".join(str(e).splitlines())

    def parse(self, outputFile):
        try:
            if self.client.ping():
                for index in self.client.indices.get('*'):
                    res = self.client.search(
                        index=index, body={'query': {'match_all': {}}})
                    outputFile.write("Index %s\n\n" % (index))
                    outputFile.write(dumps(res, indent=2))
                    outputFile.write("\n\n")
        except Exception as e:
            outputFile.write(" ".join(str(e).splitlines()))
