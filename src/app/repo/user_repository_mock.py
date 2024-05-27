from typing import Dict, Optional, List

from ..entities.user import User

from .user_repository_interface import IUserRepository

class UserRepositoryMock(IUserRepository):
    users: Dict[int, User]

    def __init__(self):
        self.users = {
            0: User(name="Vitor Soller", agency="0000", account="00000-0", current_balance=1000.0),
        }

    def get_user(self) -> Optional[User]:
        return self.users[0];