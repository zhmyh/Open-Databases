import argparse
import os
import threading
from json import load
from pathlib import Path

from tqdm import tqdm

from classes.BE import BE
from classes.CassandraHelper import CassandraHelper
from classes.CouchHelper import CouchHelper
from classes.ElasticHelper import ElasticHelper
from classes.MemcachedHelper import MemcachedHelper
from classes.MongoHelper import MongoHelper
from classes.MysqlHelper import MysqlHelper
from classes.PostgreHelper import PostgreHelper
from classes.RedisHelper import RedisHelper
from classes.Shodan import Shodan

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

CLASSES = {
    'elastic': ElasticHelper,
    'mongodb': MongoHelper,
    'couchdb': CouchHelper,
    'cassandra': CassandraHelper,
    'memcached': MemcachedHelper,
    'redis': RedisHelper,
    'postgresql': PostgreHelper,
    'mysql': MysqlHelper
}

parser = argparse.ArgumentParser()

parser.add_argument('-g', "--gather", help="Gather IP", action='store_true')
parser.add_argument('-c', "--check", help="Check IP", action='store_true')
parser.add_argument('-p', "--parse", help="Parse IP", action='store_true')
parser.add_argument('-s', "--services", help="List of available services",
                    choices=CLASSES.keys(), required=True, nargs='+')
parser.add_argument('-co', "--countries", help="Use this country (country code)",
                    nargs="+", type=str, required=True)

args = parser.parse_args()


def writeIp(service, ip, country, folder):
    outputFolder = f'{CONFIG["PATHS"]["CHECKED"]}/{folder}'
    Path(outputFolder).mkdir(parents=True, exist_ok=True)
    with open(f"{outputFolder}/{service}_{country}.txt", 'a+', encoding="utf-8") as output:
        output.write(f"{ip}\n")


def parseSingle(service, country):
    srcFileName = f'{CONFIG["PATHS"]["CHECKED"]}/good/{service}_{country}.txt'
    with open(srcFileName, 'r') as src:
        lines = src.readlines()
        outputhPath = '%s/%s/%s' % (CONFIG["PATHS"]
                                    ["PARSED"], service, country)
        for ip in tqdm(lines, desc='Parsing ' + srcFileName):
            ip = ip.strip()
            fileName = '%s.txt' % (ip.replace(":", "_"))
            Path(outputhPath).mkdir(parents=True, exist_ok=True)
            with open("%s/%s" % (outputhPath, fileName), 'w+', encoding="utf-8") as out:
                initiatedClass = CLASSES[service](ip)
                initiatedClass.parse(out)


def checkSingle(service, country):
    srcFileName = f'{CONFIG["PATHS"]["GATHERED"]}/{service}_{country}.txt'
    with open(srcFileName, 'r') as src:
        lines = src.readlines()
        for ip in tqdm(lines, desc='Checking ' + srcFileName):
            ip = ip.strip()
            initiatedClass = CLASSES[service](ip)
            response = initiatedClass.check()
            if response is True:
                writeIp(service, ip, country, 'good')
            else:
                writeIp(service, f'{ip} Error:{response}', country, 'bad')


def process(function, services, countries):
    threads = list()
    for service in services:
        for country in countries:
            x = threading.Thread(target=function, args=(service, country))
            threads.append(x)
            x.start()


def gatherResult(services):
    result = {}
    BEClient = BE(CONFIG["API_KEYS"]["BE_API_KEY"])
    ShodanClient = Shodan(CONFIG["API_KEYS"]["SHODAN_API_KEY"])
    for service in services:
        result[service] = {}
        for country in args.countries:
            result[service][country] = set()
            customQuery = CONFIG["CUSTOM_SEARCH_QUERY"][service] if service in CONFIG["CUSTOM_SEARCH_QUERY"] else 'product:%s' % (
                service)
            for i in range(1, CONFIG["LIMITS"]["be_page_limit"]):
                queryRes = BEClient.search(
                    country, customQuery, page=i)['events']
                if queryRes:
                    result[service][country].update(
                        ip['target']['ip'] for ip in queryRes)
                else:
                    break
            result[service][country].update(
                ip['ip_str'] for ip in ShodanClient.search(country, customQuery))
            with open(f'{CONFIG["PATHS"]["GATHERED"]}/{service}_{country}.txt', 'w+', encoding='UTF-8') as out:
                out.write(("\n".join(str(item)
                                     for item in result[service][country] if ":" not in item)))


def main():
    with open(f"{FILE_DIR}/config.json", 'r') as jsonConfig:
        global CONFIG
        CONFIG = load(jsonConfig)

    for key, folder in CONFIG['PATHS'].items():
        CONFIG['PATHS'][key] = '%s/%s' % (FILE_DIR, folder)
        Path(CONFIG['PATHS'][key]).mkdir(parents=True, exist_ok=True)

    if args.gather:
        gatherResult(args.services)
    if args.check:
        process(checkSingle, args.services, args.countries)
    if args.parse:
        process(parseSingle, args.services, args.countries)


if __name__ == "__main__":
    main()
