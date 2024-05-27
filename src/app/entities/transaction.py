from typing import Tuple
from ..errors.entity_errors import ParamNotValidated

class Transaction:
    method: str
    value: float
    current_balance: float
    timestamp: float

    def __init__(self, method: str=None, value: float=None, current_balance: float=None, timestamp: float=None):
        validation_method = self.validate_method(method)
        if validation_method[0] is False:
            raise ParamNotValidated("method", validation_method[1])
        self.method = method

        validation_value = self.validate_value(value, current_balance)
        if validation_value[0] is False:
            raise ParamNotValidated("value", validation_value[1])
        self.value = value

        validation_current_balance = self.validate_current_balance(current_balance)
        if validation_current_balance[0] is False:
            raise ParamNotValidated("current_balance", validation_current_balance[1])
        self.current_balance = current_balance

        validation_timestamp = self.validate_timestamp(timestamp)
        if validation_timestamp[0] is False:
            raise ParamNotValidated("timestamp", validation_timestamp[1])
        self.timestamp = timestamp

    @staticmethod
    def validate_method(method: str) -> Tuple[bool, str]:
            if method is None:
                return (False, "method is required")
            if type(method) != str:
                return (False, "method must be a string")
            if method != "deposit" and method != "withdraw":
                return (False, "method must be either deposit or withdraw")
            return (True, "")

    @staticmethod
    def validate_value(value: float, current_balance: float) -> Tuple[bool, str]:
            if value is None:
                return (False, "Value is required")
            if type(value) != float:
                return (False, "Value must be a float")
            if value < 0:
                return (False, "Value must be a positive number")
            if value >= current_balance*2:
                return (False, "Dubious deposit")
            return (True, "")
        
    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
            if current_balance is None:
                return (False, "current_balance is required")
            if type(current_balance) != float:
                return (False, "current_balance must be a float")
            if current_balance < 0:
                return (False, "current_balance must be a positive number")
            return (True, "")
        
    @staticmethod
    def validate_timestamp(timestamp: float) -> Tuple[bool, str]:
            if timestamp is None:
                return (False, "timestamp is required")
            if type(timestamp) != float:
                return (False, "timestamp must be a float")
            if timestamp < 0:
                return (False, "timestamp must be a positive number")
            return (True, "")
    
    def to_dict(self):
        return {
            "method": self.method,
            "value": self.value,
            "current_balance": self.current_balance,
            "timestamp": self.timestamp
        }
        
    def __eq__(self,other):
            return self.method == other.method and self.value == other.value and self.current_balance == other.current_balance and self.timestamp == other.timestamp
        
    def __repr__(self):
            return f"Item(method={self.method}, value={self.value}, current_balance={self.current_balance}, timestamp={self.timestamp})"