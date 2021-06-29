## Open databases

This project is developed for learning purposes and currently is open-source tool for finding open databases using Shodan and BinaryEdge and trying to download all data from found database

## Requirements

- Python 3.8

### Currently supported databases

- Cassandra
- CouchDB
- ElasticSearch
- MongoDB
- MySQL
- PostgreSQL
- Redis
- Memcached

## Config file

You need to rename file **config.json.example** to **config.json**. Config file properties:
- PATHS
    - GATHERED - folder where gathered IP's should be stored
    - CHECKED - folder where checked IP's should be stored
    - PARSED - folder where parsed IP's should be stored
- API_KEYS - if you want to use one of services, just left default value in config file
    - SHODAN_API_KEY - Shodan API key
    - BE_API_KEY - BinaryEdge API key
- CUSTOM_SEARCH_QUERY - all supported service can be found in source code or running tool with -h argument
    - service - use custom filter on BinaryEdge and Shodan to query specific service
- LIMITS
    - be_page_limit - how many pages parse on BinaryEdge

## Example usage

Gather and check only MySQL databases in Lithuania

```
py main.py -g -c -s mysql -co lt
```

## Contributing

You can contribute this project by making pull request to this project. After review I will merge this into master branch

### TODO

- [ ] Add more services
- [x] Make possible to gather data only from Shodan or BinaryEdge
- [ ] Review requirements file
- [ ] Standardize output from databases
