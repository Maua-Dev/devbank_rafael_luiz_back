import time
from fastapi.exceptions import HTTPException
import pytest
from src.app.entities.item import Item
from src.app.enums.item_type_enum import ItemTypeEnum
from src.app.main import create_deposit, create_withdraw, get_all_items, get_history, get_item, create_item, delete_item, get_user, update_item
from src.app.repo.item_repository_mock import ItemRepositoryMock
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.repo.user_repository_mock import UserRepositoryMock

class Test_Main:
    def test_get_user(self):
        repo = UserRepositoryMock()
        response = get_user()
        assert response == {
            "name": "Vitor Soller", 
            "agency":"0000", 
            "account":"00000-0", 
            "current_balance":1000
        }

    def test_create_deposit(self):
        repo = UserRepositoryMock()

        body = {
            "2": 1,
            "5": 2,
            "10": 0,
            "20": 0,
            "50": 0 ,
            "100": 0,
            "200": 0
        }
        response = create_deposit(request=body)
        print(response)
        assert response["current_balance"][0] == 1012

    def test_create_withdraw(self):
            repo = UserRepositoryMock()

            body = {
                "2": 1,
                "5": 2,
                "10": 0,
                "20": 0,
                "50": 0 ,
                "100": 0,
                "200": 0
            }
            response = create_withdraw(request=body)
            print(response)
            assert response["current_balance"][0] == 988

    def test_get_history(self):
        repo = TransactionRepositoryMock()
        response = get_history()
        print(response)
        assert response == {'all_transactions': [{'method': 'deposit', 'value': 100.0, 'current_balance': 1000.0, 'timestamp': 1690482853890.0}, {'method': 'withdraw', 'value': 300.0, 'current_balance': 700.0, 'timestamp': 1691707985704.6152}, {'method': 'deposit', 'value': 10.0, 'current_balance': 710.0, 'timestamp': 1691707990727.101}, {'method': 'withdraw', 'value': 30.0, 'current_balance': 680.0, 'timestamp': 1691707994750.5022}]}

    def test_get_all_items(self):
        repo = ItemRepositoryMock()
        response = get_all_items()
        assert all([item_expect.to_dict() == item for item_expect, item in zip(repo.items.values(), response.get("items"))]) 
        
    def test_get_item(self):
        repo = ItemRepositoryMock()
        item_id = 1
        response = get_item(item_id=item_id)
        assert response == {
            'item_id' : item_id,
            'item': repo.items.get(item_id).to_dict()
        }
        
    def test_get_item_id_is_none(self):
        
        item_id = None
        with pytest.raises(HTTPException) as err:
            get_item(item_id=item_id)
    
    def test_get_item_id_is_not_int(self):
        item_id = '1'
        with pytest.raises(HTTPException) as err:
            get_item(item_id=item_id)
            
    def test_get_item_id_is_not_positive(self):
        item_id = -1
        with pytest.raises(HTTPException) as err:
            get_item(item_id=item_id)
            
    def test_create_item(self):
        repo = ItemRepositoryMock()
        
        body = {
            'item_id': 0,
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        response = create_item(request=body)
        assert response == {'item_id': 0,'item': {'admin_permission': False, 'item_type': 'TOY', 'name': 'test', 'price': 1.0}}
    
    def test_create_item_conflict(self):
        repo = ItemRepositoryMock()
        
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
    
    def test_create_item_missing_id(self):
        body = {
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        
    def test_create_item_id_is_not_int(self):
        body = {
            'item_id': '0',
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
    
    def test_create_item_id_is_not_positive(self):
        body = {
            'item_id': -1,
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_missing_type(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_item_type_is_not_string(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'item_type': 1,
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_item_type_is_not_valid(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'item_type': 'test',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_param_not_validated(self):
        body = {
            'item_id': 1,
            'name': '',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_delete_item(self):
        body = {
            "item_id": 1
        }
        response = delete_item(request=body)
        assert response == {'item_id': 1, 'item': {'name': 'Barbie', 'price': 48.9, 'item_type': 'TOY', 'admin_permission': False}}
        
    def test_delete_item_missing_id(self):
        with pytest.raises(HTTPException) as err:
            delete_item(request={})
            
    def test_delete_item_id_is_not_int(self):
        body = {
            "item_id": '1'
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_delete_item_id_not_found(self):
        body = {
            "item_id": 100
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_delete_item_id_not_positive(self):
        body = {
            "item_id": -100
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_delete_item_without_admin_permission(self):
        body = {
            "item_id": 4
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_update_item(self):
        body = {
            "item_id": 2,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        response = update_item(request=body)
        assert response == {'item_id': 2, 'item': {'name': 'test', 'price': 1.0, 'item_type': 'TOY', 'admin_permission': False}}
        
    def test_update_item_missing_id(self):
        body = {
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
    
    def test_update_item_id_is_not_int(self):
        body = {
            "item_id": "1",
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_not_positive(self):
        body = {
            "item_id": -1,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_not_found(self):
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_without_admin_permission(self):
        body = {
            "item_id": 4,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
    
    def test_update_item_type_not_string(self):
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": 1,
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_type_not_valid(self):
        
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            