# http://127.0.0.1:5000/api/v1/hello-world-10

from wsgiref.simple_server import make_server


from flask import Blueprint, request, Flask
from flask import abort
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError

from flaskProject.api.schemas import *
from flaskProject.sql.mock_objects import *

Session = sessionmaker(bind=engine)

session = Session()

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/api/v1/hello-world-10')
def hello_world():
    return 'Hello World! 10'


@app.route('/user', methods=['POST', 'PUT'])
def register_user():
    data = request.json
    if request.method == 'POST':
        try:
            user_data = {'username': data['username'],
                         'password': bcrypt.generate_password_hash(data['password']).decode('utf-8', 'ignore'),
                         'email': data['email']}

            user = UserData().load(user_data)
        except ValidationError:
            return abort(400, 'Bad request')

        session.add(user)
        session.commit()
        return 'Successfully registered'
    if request.method == 'PUT':
        user = session.query(User).filter(User.id == data['id']).one_or_none()
        username = data['username']
        password = data['password']
        email = data['email']

        if user is None:
            abort(404, 'Event does not exist')
        else:
            user.username = username
            user.password = password
            user.email = email
            session.add(user)
            session.commit()
            result = UserData().dump(user)
            return result


@app.route('/user/<username>', methods=['GET'])
def get_user_by_username(username):
    data = UserData()
    user = session.query(User).filter(User.username == username).one_or_none()
    if user is None:
        abort(404, 'Event does not exist')
    result = data.dump(user)
    return result


@app.route('/events', methods=['GET', 'POST', 'PUT'])
def make_events():
    data = request.json

    if request.method == 'GET':
        events = session.query(Event).all()
        res = EventData(many=True).dump(events)
        result = {i: res[i] for i in range(0, len(res))}
        return result

    if request.method == 'POST':
        try:
            author_id = session.query(User).filter(User.id == data['author']).one_or_none()
            event_data = Event(data['name'], data['date'], data['description'], author_id)
        except ValidationError:
            return abort(400, 'Bad request')

        session.add(event_data, author_id)
        session.commit()
        return 'Event added'

    if request.method == 'PUT':
        event = session.query(Event).filter(Event.id == data['id']).one_or_none()
        name = data['name']
        date = data['date']
        description = data['description']

        if event is None:
            abort(404, 'Event does not exist')
        else:
            event.name = name
            event.date = date
            event.description = description
            session.add(event)
            session.commit()
            result = EventData().dump(event)
            return result

@app.route('/events/<id>', methods=['GET', 'DELETE'])
def get_event_by_id(id):
    if request.method == 'GET':
        event = session.query(Event).filter(Event.id == id).one_or_none()
        if event is None:
            abort(404, 'Event does not exist')
        result = EventData().dump(event)
        return result
    if request.method == 'DELETE':
        event = session.query(Event).filter(Event.id == id).one_or_none()
        if event is None:
            abort(404, 'Event does not exist')
        session.delete(event)
        session.commit()
        return 'Deleted successfully'


@app.route('/events/connectedEvents/<author_id>', methods=['GET'])
def get_connected_events(author_id):
    events = session.query(Event).filter(Event.author_id == author_id).all()
    if events is None:
        abort(404, 'Event does not exist')
    res = EventData(many=True).dump(events)
    result = {i: res[i] for i in range(0, len(res))}
    return result


if __name__ == '__main__':
    app.run()

server = make_server('', 5000, app)
server.serve_forever()


#curl -XPOST http://127.0.0.1:5000/user -H "Content-Type:application/json" --data "{\"username\":\"John\", \"password\":\"8462927\", \"email\":\"johnd@email.com\"}"
#curl -XPUT http://127.0.0.1:5000/user -H "Content-Type:application/json" --data "{\"id\":\"1\", \"username\":\"John\", \"password\":\"202fjduy\", \"email\":\"johnd22@email.com\"}"
#curl -XGET http://127.0.0.1:5000/user/John

#curl -XPOST http://127.0.0.1:5000/events -H "Content-Type:application/json" --data "{\"name\":\"Movie night\", \"date\":\"2020-12-20\", \"description\":\"Popcorn\", \"author\":\"2\"}"
#curl -XPUT http://127.0.0.1:5000/events -H "Content-Type:application/json" --data "{\"id\":\"2\", \"name\":\"Movie night\", \"date\":\"2020-12-21\", \"description\":\"Popcorn(remember)\"}"
#curl -XGET http://127.0.0.1:5000/events
#curl -XGET http://127.0.0.1:5000/events/connectedEvents/2