from typing import Dict, Optional, Union

class MediaFile:
    id: int
    bcode: int

    def copy(self):
        mf = MediaFile()
        mf.id = self.id
        mf.bcode = self.bcode
        return mf

class MediaFiles:
    owner: int #cafeid
    det: str #photo or video
    # file_id -> File
    _files: Dict[int, MediaFile]


    def __init__(self, det:str):
        self._files = {}
        self.det = det

    def get(self, fid: int) -> Optional[MediaFile]:
        cc = self._files.get(fid)
        return MediaFiles._copy_if_none(cc)

    def put(self, mf: MediaFile) -> int:
        if MediaFile.id is None:
            MediaFile.id = len(self._files) + 1
        #To dict
        self._files[mf.id] = mf
        return mf.id

    @staticmethod
    def _copy_if_none(mf):
        if mf is not None:
            return mf.copy()
        else:
            return None