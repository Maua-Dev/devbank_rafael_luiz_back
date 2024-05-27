from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def get_user(self) -> Optional[User]:
        '''
        Returns the first user in database
        '''
        pass