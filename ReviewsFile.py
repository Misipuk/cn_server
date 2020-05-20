from typing import Dict, Optional, Union

class Review:
    id: int
    owner: str  #ownerlogin
    cafeid: int
    stars: int
    time: int
    description: str #login, review

    def __init__(self):
        pass

    def __init__(self, owner: str, cafeid: int, stars:int, desc: str):
        self.owner = owner
        self.cafeid = cafeid
        self.stars = stars
        self.description = desc

    def copy(self):
        r = Review()
        r.id = self.id
        r.owner = self.owner
        r.cafeid = self.cafeid
        r.stars = self.stars
        r.time = self.time
        r.description = self.description
        return r


class Rewiews:
    # cafe_id -> Reviews
    _cafe_rewiews: Dict[int, list[Review]]
    # user_login -> UserReviews
    _login_reviews: Dict[str, list[Review]]
    _allreviews = list[Review]

    def __init__(self):
        self._cafe_rewiews = {}
        self._login_reviews = {}
        self._allreviews = []
        r1 = Review('PanAleha', 3, 5, 'Вкусный осетр')
        r2 = Review('PanAleha', 1, 3,'Ребята, пирожки у них просто невероятные!')
        r3 = Review('VasyaPupkin', 1, 5, 'Мясная пицца лучшая :)')
        r4 = Review('VasyaPupkin', 2, 5, 'У них на сцене поющая уточка, вечер удался)))')
        r5 = Review('LesyaSuper', 2, 2, 'Долго обслуживали, разве что крякали прикольно')
        r6 = Review('LesyaSuper', 3, 1, 'Да это не из осетра, а из карася!!!')
        r7 = Review('MrMops', 3, 5, 'Изысканная кухня')
        r8 = Review('MrMops', 1, 4, 'Пирожок был еле теплый, но все равно вкусно')
        self.put(r1)
        self.put(r2)
        self.put(r3)
        self.put(r4)
        self.put(r5)
        self.put(r6)
        self.put(r7)
        self.put(r8)

    def get_by_cafe(self, cid: int) -> Optional[list[Review]]:
        rvs = self._cafe_rewiews.get(cid)
        return Rewiews._copy_if_none(rvs) if rvs is not None else None

    def get_by_login(self, login: str) -> Optional[list[Review]]:
        rvs = self._login_reviews.get(login)
        return Rewiews._copy_if_none(rvs) if rvs is not None else None

    def put(self, review: Review) -> int:
        if review.id is None:
            if self._allreviews is not None:
                review.id = self._allreviews[-1].id + 1
            else:
                review.id = 1

        #To list
        if self._allreviews is not None:
            self._allreviews.append(review)
        else:
            self._allreviews = [review]


        #To dict
        if self._cafe_rewiews.get(review.cafeid) is not None:
            self._cafe_rewiews[review.cafeid] = self._cafe_rewiews[review.cafeid] + [review]
        else:
            self._cafe_rewiews[review.cafeid] = [review]

        if self._login_reviews.get(review.owner) is not None:
            self._login_reviews[review.owner] = self._login_reviews[review.owner] + [review]
        else:
            self._login_reviews[review.owner] = [review]
        return review.id

    def del_by_userlogin(self, login: str, revid:int):
        for rev in self._allreviews:
            if rev.id == revid and rev.owner == login:
                self._cafe_rewiews.get(rev.cafeid).remove(rev) #QUESTION
                self._login_reviews.get(login).remove(rev)
                self._allreviews.remove(rev)
                return 1
            else:
                return -1


    @staticmethod
    def _copy_if_none(rvs: list[Review]):
        if rvs is not None:
            rvs1 = []
            for r in rvs:
                rvs1.append(r.copy())
            return rvs1
        else:
            return None