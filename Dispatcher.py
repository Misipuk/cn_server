from CafesFile import Cafes
from HandlerFile import Users, Handler
from MediaFileClass import MediaFiles
from MyHTTPServerFile import MyHTTPServer
from ReviewsFile import Reviews
from UsersFile import User


def fill_users(users: Users):
    u1 = User('PizzaOwner', 'lovepizza1')
    u2 = User('PubOwner', 'lovepub1')
    u3 = User('SushiOwner', 'lovesushi1')
    u4 = User('VasyaPupkin', 'lovepupok1')
    u5 = User('PanAleha', 'loveAleha1')
    u6 = User('LesyaSuper', 'loveLesya1')
    u7 = User('MrMops', 'loveMops1')
    users.put(u1)
    users.put(u2)
    users.put(u3)
    users.put(u4)
    users.put(u5)
    users.put(u6)
    users.put(u7)


if __name__ == '__main__':
    host = ''
    port = 9091
    name = 'MyServer'

    users = Users()
    cafes = Cafes()
    media_files = MediaFiles()
    cafe_reviews = Reviews()

    fill_users(users)

    handler = Handler(users, cafes, media_files, cafe_reviews)

    serv = MyHTTPServer(host, port, name, handler)
    try:
        serv.serve_forever()
    except Exception as e:
        print('Serving failed', e)

# TODO:
# 1. replace len(...) in repositories (CafesFile, ...)
