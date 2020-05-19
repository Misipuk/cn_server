from typing import Dict, Optional, Union

class Review:
    id: int
    owner: str  #ownerlogin
    cafeid: int
    description: str

    def copy(self):
        r = Review()
        r.id = self.id
        r.owner = self.owner
        r.cafeid = self.cafeid
        r.description = self.description
        return r

class Rewiews:
    # cafe_id -> ReviewsList
    _rewiews: Dict[int, ]
    # login -> cafe_id
    _owner_login: Dict[str, int]

    def __init__(self):
        self._cafes = {}
        self._owner_login = {}

    def get(self, uid: int) -> Optional[Cafe]:
        cc = self._cafes.get(uid)
        return Cafes._copy_if_none(cc)

    def get_by_login(self, login: str) -> Optional[Cafe]:
        uid = self._owner_login.get(login)
        return self.get(uid) if uid is not None else None

    def put(self, cafe: Cafe) -> int:
        if cafe.id is None:
            cafe.id = len(self._cafes) + 1
        #To dict
        self._cafes[cafe.id] = cafe
        self._owner_login[cafe.login] = cafe.id

        return cafe.id

    @staticmethod
    def _copy_if_none(cafe):
        if cafe is not None:
            return cafe.copy()
        else:
            return None