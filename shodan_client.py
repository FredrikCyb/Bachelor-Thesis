import shodan
from shodan_interface import ShodanInterface

class ShodanClient(ShodanInterface):
    def __init__(self, api_key: str):
        self.api = shodan.Shodan(api_key)

    def search(self, query: str) -> dict:
        return self.api.search(query)
    
    def host(self, host: str) -> dict:
        return self.api.host(host)