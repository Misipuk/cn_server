import base64
import hashlib
import json
import time
from typing import Dict, Optional, Union

from HTTPErrorFile import HTTPError
from RequestFile import Request
from ResponseFile import Response

secret = "jdfkgahlskjhflkj2y3iy187 2rofiulh"


def sha256(s: str) -> bytes:
    m = hashlib.sha256()
    m.update(s.encode())
    return m.digest()


def b64_encode(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b)


def b64_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s.encode())


class Token:
    login: str
    expire: int
    key: str

    def __init__(self, login: str, expire: int):
        self.login = login
        self.expire = expire
        self.key = b64_encode(sha256(login + "|" + str(expire) + "|" + secret)).decode()

    @staticmethod
    def as_token(authorization: str) -> Optional[str]:
        decoded = b64_decode(authorization).decode()
        d = json.loads(decoded)
        expected_key = Token(d["login"], d["expire"]).key

        if d["key"] != expected_key:
            raise Exception("invalid key")
        if d["expire"] < int(time.time()):
            raise Exception("token expired")

        return d["login"]

    @staticmethod
    def as_authorization(login: str, expire: int) -> str:
        token = Token(login, expire)
        token = json.dumps(token.__dict__)
        return b64_encode(token.encode()).decode()


class User:
    id: int
    login: str
    # TODO: keep hashed?
    password: str

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


class Handler:

    def __init__(self, users: Users):
        self._users = users

    def handle_request(self, req: Request):
        user_login = None
        if "Authorization" in req.headers:
            try:
                user_login = Token.as_token(req.headers["Authorization"])
            except KeyError as ke:
                return HTTPError(403, "Forbidden", body=("token must have key " + str(ke)).encode())
            except Exception as e:
                return HTTPError(403, "Forbidden", body=str(e).encode())

        if req.path == '/users' and req.method == 'POST':
            return self.handle_post_users(req)

        if req.path == '/login' and req.method == 'POST':
            return self.handle_login_user(req)

        if req.path == '/users' and req.method == 'GET':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_users(req, user_login)

        if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)

        raise HTTPError(404, 'Not found')

    def handle_post_users(self, req):
        user = self.read_user_from_request_body(req)
        _ = self._users.put(user)
        user = user.copy()

        user.password = None
        return Response(204, 'Created', body=user)

    def handle_get_users(self, req, user_login: str):
        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Пользователи ({len(self._users._users)})</div>'
            body += '<ul>'
            for u in self._users._users.values():
                body += f'<li>#{u["id"]} {u["login"]}, {u["age"]}</li>'
            body += '</ul>'
            body += '</body></html>'

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(self._users.__dict__)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_get_user(self, req, user_id):
        user = self._users.get(int(user_id))
        if not user:
            raise HTTPError(404, 'Not found')

        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'#{user["id"]} {user["name"]}, {user["age"]}'
            body += '</body></html>'

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(user)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return HTTPError(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = {'Content-Type': contentType,
                   'Content-Length': len(body)}
        return Response(200, 'OK', headers, body)

    def handle_login_user(self, req: Request) -> Union[Response, HTTPError]:
        user_from_req = self.read_user_from_request_body(req)
        user_from_db = self._users.get_by_login(user_from_req.login)

        if user_from_db is None:
            # user not found, 404
            return HTTPError(404, 'Not Found')

        if user_from_db.password != user_from_req.password:
            # forbidden, 403
            return HTTPError(403, 'Forbidden')

        ts = int(time.time())
        token = Token.as_authorization(user_from_db.login, ts + 3600)
        return Response(200, 'OK', headers={"Authorization": token})

    @staticmethod
    def read_user_from_request_body(req) -> User:
        bb = req.body()
        print(bb)
        body = json.loads(bb)
        print("body: " + str(body))

        user = User()
        user.id = None
        user.login = body["login"]
        user.password = body["password"]
        return user
