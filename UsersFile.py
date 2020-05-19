from typing import Dict, Optional, Union

class User:
    id: int
    login: str
    # TODO: keep hashed?
    password: str

    def __init__(self):
        pass

    def __init__(self, id: int, login: str, password: str):
        self.id = id
        self.login = login
        self.password = password

    def copy(self):
        u = User()
        u.id = self.id
        u.login = self.login
        u.password = self.password
        return u


class Users:
    # user_id -> User
    _users: Dict[int, User]
    # login -> user_id
    _users_login: Dict[str, int]

    def __init__(self):
        self._users = {}
        self._users_login = {}
        u1 = User(1, 'PizzaOwner', 'lovepizza1')
        u2 = User(2, 'PubOwner', 'lovepub1')
        u3 = User(3, 'SushiOwner', 'lovesushi1')
        u4 = User(4, 'VasyaPupkin', 'lovepupok1')
        u5 = User(1, 'PanAleha', 'loveAleha1')
        self.put(u1);
        self.put(u2);
        self.put(u3);
        self.put(u4);
        self.put(u5);


    def get(self, uid: int) -> Optional[User]:
        uu = self._users.get(uid)
        return Users._copy_if_none(uu)

    def get_by_login(self, login: str) -> Optional[User]:
        uid = self._users_login.get(login)
        return self.get(uid) if uid is not None else None

    def put(self, user: User) -> int:
        if user.id is None:
            user.id = len(self._users) + 1

        self._users[user.id] = user
        self._users_login[user.login] = user.id

        return user.id

    @staticmethod
    def _copy_if_none(user):
        if user is not None:
            return user.copy()
        else:
            return None