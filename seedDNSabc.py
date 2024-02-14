from abc import ABC, abstractmethod

class seedDNS(ABC):
    @abstractmethod
    def top1m(): pass
    @abstractmethod
    def fmtfile(): pass
    @abstractmethod
    def consult(dns, mode, type): pass