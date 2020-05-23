from CafesFile import Cafes, Cafe
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

def fill_cafes(cafes: Cafes):
     c1 = Cafe('PizzaOwner', 'PizzaDay', 'Very tasty pizza', 'Dnepr')
     c2 = Cafe('PubOwner', 'Duck Pub', 'We have cool tea', 'Kiev')
     c3 = Cafe('SushiOwner', 'Sushi Iz Karasya', 'Only Japan Fish', 'Cherkasi')
     cafes.put(c1)
     cafes.put(c2)
     cafes.put(c3)


if __name__ == '__main__':
    host = ''
    port = 9091
    name = 'MyServer'

    users = Users()
    cafes = Cafes()
    media_files = MediaFiles()
    cafe_reviews = Reviews()

    fill_users(users)
    fill_cafes(cafes)

    handler = Handler(users, cafes, media_files, cafe_reviews)

    serv = MyHTTPServer(host, port, name, handler)
    try:
        serv.serve_forever()
    except Exception as e:
        print('Serving failed', e)

# TODO:
# 1. replace len(...) in repositories (CafesFile, ...)
