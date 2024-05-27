import time
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .environments import Environments

from .repo.item_repository_mock import ItemRepositoryMock
from .repo.user_repository_mock import UserRepositoryMock
from .repo.transaction_repository_mock import TransactionRepositoryMock

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item
from .entities.user import User
from .entities.transaction import Transaction

app = FastAPI()

repo = Environments.get_item_repo()()
user_repo = Environments.get_user_repo()()
transaction_repo = Environments.get_transaction_repo()()

@app.get("/get_user")
def get_user():
    user = user_repo.get_user()
    return {
        "name": user.name,
        "agency": user.agency,
        "account": user.account,
        "current_balance": user.current_balance
    }

@app.post("/create_deposit", status_code=201)
def create_deposit(request: dict):
    values = 0
    user_repo = UserRepositoryMock()

    for key, value in request.items():
        value = int(key)*value
        values += value
    
    float_values = float(values)

    validation_value = Transaction.validate_value(value=float_values, current_balance=user_repo.users[0].current_balance)
    
    if not validation_value[0]:
        raise HTTPException(status_code=403, detail=validation_value[1])

    value=float_values,
    current_balance= (user_repo.users[0].current_balance + float_values),
    timestamp= time.time(),

    deposit_response = transaction_repo.create_deposit(value, current_balance, timestamp)
    print(deposit_response)
    return {
        "current_balance": current_balance,
        "timestamp": timestamp    
    }

@app.post("/create_withdraw", status_code=201)
def create_withdraw(request: dict):
    values = 0
    user_repo = UserRepositoryMock()

    for key, value in request.items():
        value = int(key)*value
        values += value
    
    float_values = float(values)

    validation_value = Transaction.validate_value(value=float_values, current_balance=user_repo.users[0].current_balance)
    
    if not validation_value[0]:
        raise HTTPException(status_code=403, detail=validation_value[1])

    value=float_values,
    current_balance= (user_repo.users[0].current_balance - float_values),
    timestamp= time.time(),

    deposit_response = transaction_repo.create_deposit(value, current_balance, timestamp)
    print(deposit_response)
    return {
        "current_balance": current_balance,
        "timestamp": timestamp    
    }

@app.get("/get_history")
def get_history():
    transactions = transaction_repo.get_history()
    return {
        "all_transactions": [transaction.to_dict() for transaction in transactions]
    }

@app.get("/items/get_all_items")    
def get_all_items():
    items = repo.get_all_items()
    return {
        "items": [item.to_dict() for item in items]
    }

@app.get("/items/get_all_items")
def get_all_items():
    items = repo.get_all_items()
    return {
        "items": [item.to_dict() for item in items]
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }

@app.post("/items/create_item", status_code=201)
def create_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    if item is not None:
        raise HTTPException(status_code=409, detail="Item already exists")
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    if item_type is None:
        raise HTTPException(status_code=400, detail="Item type is required")
    if type(item_type) != str:
        raise HTTPException(status_code=400, detail="Item type must be a string")
    if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
        raise HTTPException(status_code=400, detail="Item type is not a valid one")
    
    admin_permission = request.get("admin_permission")
    
    try:
        item = Item(name=name, price=price, item_type=ItemTypeEnum[item_type], admin_permission=admin_permission)
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=err.message)
    
    item_response = repo.create_item(item, item_id)
    return {
        "item_id": item_id,
        "item": item_response.to_dict()    
    }
    
@app.delete("/items/delete_item")
def delete_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    if item.admin_permission == True:
        raise HTTPException(status_code=403, detail="Item Not found")
    
    item_deleted = repo.delete_item(item_id)
    
    return {
        "item_id": item_id,
        "item": item_deleted.to_dict()    
    }
    
@app.put("/items/update_item")
def update_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    if item.admin_permission == True:
        raise HTTPException(status_code=403, detail="Item Not found")
    
    name = request.get("name")
    price = request.get("price")
    admin_permission = request.get("admin_permission")
    
    item_type_value = request.get("item_type")
    if item_type_value != None:
        if type(item_type_value) != str:
            raise HTTPException(status_code=400, detail="Item type must be a string")
        if item_type_value not in [possible_type.value for possible_type in ItemTypeEnum]:
            raise HTTPException(status_code=400, detail="Item type is not a valid one")
        item_type = ItemTypeEnum[item_type_value]
    else:
        item_type = None
        
    item_updated = repo.update_item(item_id, name, price, item_type, admin_permission)
    
    return {
        "item_id": item_id,
        "item": item_updated.to_dict()    
    }
    


handler = Mangum(app, lifespan="off")
