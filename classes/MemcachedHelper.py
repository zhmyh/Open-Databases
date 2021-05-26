import re
import telnetlib
import json
from pymemcache.client.base import Client
import unicodedata

class MemcachedHelper:
    _key_regex = re.compile(r'ITEM (\S*)')
    _slab_regex = re.compile(r'STAT items:(.*):number')
    _stat_regex = re.compile(r"STAT (.*) (.*)\r")
    _value_regex = re.compile(r"VALUE (.*) (.*)\r")
    _client = None

    def __init__(self, host, port=11211, timeout=30):
        self._host = host
        self._port = port
        self._timeout = timeout
        self.api_client = Client((host, port), encoding="UTF-8")

    def uescape_decode(self, m):
        return ""

    def remove_control_characters(self, s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

    def check(self):
        try:
            self.command('stats')
            return True
        except  Exception as e:
            return " ".join(str(e).splitlines())

    def parse(self, outputFile):
        key_values = {}
        for key in self.keys():
            if key.isascii():
                value = self.api_client.get(key)
                key_values[key] = value if value is None else value.decode("ascii", "ignore")
        unicode_escape = re.compile(r'(?<!\\)(?:\\u([dD][89abAB][a-fA-F0-9]{2})\\u([dD][c-fC-F][a-fA-F0-9]{2})|\\u([a-fA-F0-9]{4}))')
        data = json.dumps(key_values)
        data = unicode_escape.sub(self.uescape_decode, data)
        data = self.remove_control_characters(data)
        outputFile.write(data)

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port,
                                            self._timeout)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write(("%s\n" % cmd).encode('UTF-8'))
        return self.client.read_until(b'END', timeout=5).decode('UTF-8', "ignore")

    def keys(self, limit=100):
        ' Return a list of keys in use '
        cmd = 'stats cachedump %s %s'
        return [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % (id, limit)))]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))
