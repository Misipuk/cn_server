from typing import Dict, Optional, Union
from MediaFileClass import MediaFile, MediaFiles
class Cafe:
    id: int
    owner: str  #ownerlogin
    name: str
    city: str
    photos: MediaFiles('p')
    videos: MediaFiles('v')
    description: str
    reviews: []

    def copy(self):
        c = Cafe()
        c.id = self.id
        c.owner = self.owner
        c.name = self.name
        c.city = self.city
        c.photos = self.photos
        c.videos = self.videos
        c.details = self.details
        return c

class Cafes:
    # cafe_id -> Cafe
    _cafes: Dict[int, Cafe]
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