import base64
import hashlib
import json
import time
from typing import Dict, Optional, Union

from HTTPErrorFile import HTTPError
from RequestFile import Request
from ResponseFile import Response
from TokenFile import Token
from UsersFile import User, Users




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

        #TODO
        if req.path == '/cafes' and req.method == 'GET': #withMeanStars
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_cafes(req)

        if req.path == '/cafemedia' and req.method == 'GET':#WithReviews
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_get_cafe_media(req)

        if req.path == '/delcafemedia' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_edit_cafe(req)

        if req.path == '/addcafemedia' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_add_cafe_media(req)

        if req.path == '/createcafe' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_create_cafe(req)

        if req.path == '/editcafe' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_edit_cafe(req)


        if req.path == '/addreview' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_add_review(req)

        if req.path == '/delreview' and req.method == 'POST':
            if user_login is None:
                return HTTPError(403, "Forbidden", body="authorization header is absent".encode())
            return self.handle_del_review(req)

        if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)

        raise HTTPError(404, 'Not found')

     #TODO
    def handle_get_cafes(self, req):
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(self._users.__dict__)
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_get_cafe_media(self, req):
        pass

    def handle_create_cafe(self, req):
        pass

    def handle_edit_cafe(self, req):
        pass

    def handle_del_cafe_media(self, req):
        pass

    def handle_add_review(self, req):
        pass

    def handle_del_review(self, req):
        pass

    def handle_add_cafe_media(self, req):
        pass


    def handle_post_users(self, req):
        user = self.read_user_from_request_body(req)
        _ = self._users.put(user)
        user = user.copy()

        user.password = None
        return Response(204, 'Created', body=user)

    def handle_get_users(self, req, user_login: str):
        accept = req.headers.get('Accept')

        if 'application/json' in accept:
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
        if 'application/json' in accept:
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
