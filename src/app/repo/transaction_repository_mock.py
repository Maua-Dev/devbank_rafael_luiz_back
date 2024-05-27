from typing import Dict, Optional, List

from ..entities.transaction import Transaction

from .transaction_repository_interface import ITransactionRepository

from .user_repository_mock import UserRepositoryMock

import time

class TransactionRepositoryMock(ITransactionRepository):
    transactions: Dict[int, Transaction]

    def __init__(self):
        self.transactions = {
            0: Transaction(
                method= "deposit",
                value= 100.0,
                current_balance= 1000.0,
                timestamp= 1690482853890.0),
            1: Transaction(
                method= "withdraw",
                value= 300.0,
                current_balance= 700.0,
                timestamp= 1691707985704.6152),
            2: Transaction(
                method= "deposit",
                value= 10.0,
                current_balance=  710.0,
                timestamp= 1691707990727.101),
            3: Transaction( 
                method= "withdraw",
                value= 30.0,
                current_balance= 680.0,
                timestamp= 1691707994750.5022)
        }
    
    def create_deposit(self, value: float, current_balance: float, timestamp: float) -> Transaction:
        new_transaction = Transaction(
            method="deposit",
            value=value[0],
            current_balance= current_balance[0],
            timestamp= timestamp[0],
        )

        return new_transaction
    
    def create_withdraw(self, qty: Dict) -> Transaction:
        qty_value = 0;

        for key, value in qty.items:
            qty_value += value

        new_transaction = Transaction(
            method="withdraw",
            value=qty_value,
            current_balance= (UserRepositoryMock.users[0].current_balance - qty_value),
            timestamp= round(time.time() * 1000),
        )

        return new_transaction
    
    def get_history(self) -> List[Transaction]:
        return self.transactions.values()