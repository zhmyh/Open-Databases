from pybinaryedge import BinaryEdge
import pybinaryedge

class BE:
    def __init__(self, api_key):
        self.client = BinaryEdge(api_key)

    def search(self, country, last, page=1):
        try:
            query = 'country:%s %s' % (country, last)
            return self.client.host_search(query, page)
        except pybinaryedge.api.BinaryEdgeException as e:
            return None
