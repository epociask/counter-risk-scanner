from abc import ABC, abstractmethod
 
class Analyzer(ABC):
 
    @abstractmethod
    def risk_score():
        pass

    @abstractmethod
    def assess():
        pass
