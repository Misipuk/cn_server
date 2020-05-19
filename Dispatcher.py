from HandlerFile import Users, Handler
from MyHTTPServerFile import MyHTTPServer

if __name__ == '__main__':
    host = ''
    port = 9091
    name = 'MyServer'

    users = Users()
    handler = Handler(users)

    serv = MyHTTPServer(host, port, name, handler)
    try:
        serv.serve_forever()
    except Exception as e:
        print('Serving failed', e)
