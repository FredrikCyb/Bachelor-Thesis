from abc import ABC, abstractmethod

class ShodanInterface(ABC):
    @abstractmethod
    def search(self, query: str) -> dict:
        pass
    @abstractmethod
    def host(self, host: str) -> dict:
        pass