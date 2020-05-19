from typing import Dict, Optional, Union

class Review:
    id: int
    owner: str  #ownerlogin
    cafeid: int
    time: int
    description: str #login, review

    def __init__(self):
        pass

    def copy(self):
        r = Review()
        r.id = self.id
        r.owner = self.owner
        r.cafeid = self.cafeid
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

    def get_by_cafe(self, cid: int) -> Optional[list[Review]]:
        rvs = self._cafe_rewiews.get(cid)
        return Rewiews._copy_if_none(rvs) if rvs is not None else None

    #Доделать
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


    @staticmethod
    def _copy_if_none(rvs: list[Review]):
        if rvs is not None:
            rvs1 = []
            for r in rvs:
                rvs1.append(r.copy())
            return rvs1
        else:
            return None