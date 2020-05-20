from typing import Dict, Optional, Union

class MediaFile:
    id: int
    cafeid: int
    bcode: int

    def __init__(self):
        pass

    def copy(self):
        mf = MediaFile()
        mf.id = self.id
        mf.cafeid = self.cafeid
        mf.bcode = self.bcode
        return mf

class MediaFiles:
    det: str #photo or video           folder photos or videos
    # cafe_id -> list of MediaFiles
    _cafe_files: Dict[int, list[MediaFile]]
    _all_files: list[MediaFile]


    def __init__(self, cafeid_owner: int, det:str):
        self.det = det
        self._cafe_files = {}
        self._all_files = []

    def get(self, cid: int) -> Optional[list[MediaFile]]:
        mfl = self._cafe_files.get(cid)
        # image_data = open('photos/'+mf.id, 'rb')
        # bytes = image_data.read()
        return MediaFiles._copy_if_none(mfl)

    def put(self, mf: MediaFile) -> int:
        if mf.id is None:
            if self._all_files is not None:
                mf.id = self._all_files[-1].id + 1
            else:
                mf.id = 1
        # image_data = open('photos/'+mf.id, 'rb')
        # bytes = image_data.write() ?
        #To list
        if self._all_files is not None:
            self._all_files.append(mf)
        else:
            self._all_files = [mf]

        #To dict
        if self._cafe_files.get(mf.cafeid) is not None:
            self._cafe_files[mf.cafeid] = self._cafe_files[mf.cafeid] + [mf]
        else:
            self._cafe_files[mf.cafeid] = [mf]

        return mf.id

    def delete_by_cafeid(self, cafeid:int, fileid:int):
        for mf in self._all_files:
            if mf.id == fileid and mf.cafeid == cafeid:
                self._cafe_files.get(mf.cafeid).remove(mf)  # QUESTION
                self._all_files.remove(mf)
                return 1
            else:
                return -1

    @staticmethod
    def _copy_if_none(mf: list[MediaFile]):
        if mf is not None:
            mf1 = []
            for f in mf:
                mf1.append(f.copy())
            return mf1
        else:
            return None