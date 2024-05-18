from typing import Tuple
from ..errors.entity_errors import ParamNotValidated
from ..enums.item_type_enum import ItemTypeEnum

class Transaction:
    type: str
    value: float
    current_balance: float
    timestamp: float

    def __init__(self, type: str=None, value: float=None, current_balance: float=None, timestamp: float=None):
        validation_type = self.validate_type(type)
        if validation_type[0] is False:
            raise ParamNotValidated("type", validation_type[1])
        self.type = type

        validation_value = self.validate_value(value)
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
        def validate_type(type: str) -> Tuple[bool, str]:
            if type is None:
                return (False, "Type is required")
            if type(type) != str:
                return (False, "Type must be a string")
            if type != "deposit" and type != "withdraw":
                return (False, "Type must be either deposit or withdraw")
            return (True, "")

        @staticmethod
        def validate_value(value: float) -> Tuple[bool, str]:
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
        
        def __eq__(self,other):
            return self.type == other.type and self.value == other.value and self.current_balance == other.current_balance and self.timestamp == other.timestamp
        
        def __repr__(self):
            return f"Item(type={self.type}, value={self.value}, current_balance={self.current_balance}, timestamp={self.admin_permission})"