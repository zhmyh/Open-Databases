import shodan

class Shodan:
    def __init__(self, api_key):
        self.client = shodan.Shodan(api_key)

    def search(self, country, last):
        query = 'country:%s %s' % (country, last)
        return self.client.search_cursor(query)
