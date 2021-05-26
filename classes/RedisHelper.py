import redis
import json

class RedisHelper:
    def __init__(self, ip, port=6379):
        try:
            self.client = redis.StrictRedis(host=ip, port=port, db=0, socket_timeout=30, socket_connect_timeout=30)
        except:
            pass

    def check(self):
        try:
            self.client.client_id()
            return True
        except Exception as e:
            return " ".join(str(e).splitlines())

    def parse(self, outputFile):
        result = {}
        try:
            for key in self.client.scan_iter():
                result[key.decode('utf-8')] = self.client.get(key).decode('utf-8')
            json.dump(result, outputFile)
        except Exception as e:
            outputFile.write(" ".join(str(e).splitlines()))

