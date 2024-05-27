from abc import ABC, abstractmethod
from typing import Dict

from ..entities.transaction import Transaction

class ITransactionRepository(ABC):

    @abstractmethod
    def create_deposit(self, qty: Dict) -> Transaction:
        '''
        Creates a new deposit in the database
        '''
        pass

    @abstractmethod
    def create_withdraw(self, qty: Dict) -> Transaction:
        '''
        Creates a new withdraw in the database
        '''
        pass