from typing import Dict, Optional, Union
from MediaFileClass import MediaFile, MediaFiles

class Cafe:
    id: int
    owner: str  #ownerlogin
    name: str
    city: str
#    photos: MediaFiles('p')  в базе?
#    videos: MediaFiles('v')
    description: str
#    reviews: []  легко достать в базе

    def __init__(self):
        pass

    def __init__(self, owner:str, name:str, des: str, city: str):
        self.id = None
        self.owner = owner
        self.name = name
        self.des = des


    def copy(self):
        c = Cafe()
        c.id = self.id
        c.owner = self.owner
        c.name = self.name
        c.city = self.city
        #c.photos = self.photos
        #c.videos = self.videos
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
        c1 = Cafe('PizzaOwner', 'PizzaDay', 'Очень вкусная пицца', 'Днепр')
        c2 = Cafe('PubOwner', 'Duck Pub', 'У нас классный чай', 'Киев')
        c3 = Cafe('SushiOwner', 'Sushi Iz Karasya', 'Только японские морепродукты', 'Черкасы')
        self.put(c1)
        self.put(c2)
        self.put(c3)


    def get(self, cid: int) -> Optional[Cafe]:
        cc = self._cafes.get(cid)
        return Cafes._copy_if_none(cc)

    def get_by_login(self, login: str) -> Optional[Cafe]:
        cid = self._owner_login.get(login)
        return self.get(cid) if cid is not None else None

    def edit(self, cafe: Cafe) -> Optional[Cafe]:
        c = self._cafes.get(cafe.id)
        c.name = cafe.name
        c.description = cafe.description
        return self.get(cafe.id) if cafe.id is not None else None

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