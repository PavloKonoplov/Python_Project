# http://127.0.0.1:5000/api/v1/hello-world-10

from wsgiref.simple_server import make_server

from flask import Blueprint, request, Flask, jsonify
from flask import abort
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from flask_jwt_extended import (JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity)

from flaskProject.api.schemas import *
from flaskProject.sql.mock_objects import *

Session = sessionmaker(bind=engine)

session = Session()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.route('/api/v1/hello-world-10')
def hello_world():
    return 'Hello World! 10'


@app.route('/login', methods=['POST'])
def login():
    # if not request.is_json:
    #    return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = session.query(User).filter(User.username == username).one_or_none()

    if not user:
        abort(404, 'User does not exist')

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return abort(403, 'Invalid password')


@app.route('/user', methods=['POST', 'PUT'])
@jwt_optional
def register_user():
    data = request.json
    if request.method == 'POST':
        user = UserData().load({'username': data['username'],
                                'password': bcrypt.generate_password_hash(data['password']).decode('utf-8', 'ignore'),
                                'email': data['email']})

        session.add(user)
        session.commit()
        return create_access_token(identity=user.username)
    if request.method == 'PUT':

        if not get_jwt_identity():
            abort(401, 'You need to log in')

        user = session.query(User).filter(User.id == data['id']).one_or_none()

        if user.username != get_jwt_identity():
            abort(403, 'You can only change your own account details')

        username = data['username']
        password = bcrypt.generate_password_hash(data['password']).decode('utf-8', 'ignore')
        email = data['email']

        if user is None:
            abort(404, 'User does not exist')
        else:
            user.username = username
            user.password = password
            user.email = email
            session.add(user)
            session.commit()
            # result = UserData().dump(user)
            return create_access_token(identity=username)


@app.route('/user/<username>', methods=['GET'])
def get_user_by_username(username):
    data = UserData()
    user = session.query(User).filter(User.username == username).one_or_none()
    if user is None:
        abort(404, 'User does not exist')
    result = data.dump(user)
    return result


@app.route('/events', methods=['GET', 'POST', 'PUT'])
@jwt_optional
def make_events():
    data = request.json

    if request.method == 'GET':
        events = session.query(Event).all()
        res = EventData(many=True).dump(events)
        result = {i: res[i] for i in range(0, len(res))}
        return result

    if request.method == 'POST':
        if not get_jwt_identity():
            abort(401, 'You need to log in')
        # try:
        author = session.query(User).filter(User.username == get_jwt_identity()).one_or_none()

        event_data = Event(data['name'], data['date'], data['description'], author)
        # except ValidationError:
        # return abort(400, 'Bad request')

        session.add(event_data, author)
        session.commit()
        return 'Event added'

    if request.method == 'PUT':
        author = get_jwt_identity()

        if not author:
            abort(401, 'You need to log in')

        event = session.query(Event).filter(Event.id == data['id']).one_or_none()

        if event.author.username != author:
            abort(403, 'You can only edit your own events')

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
# server.serve_forever()


# curl -XPOST http://127.0.0.1:5000/user -H "Content-Type:application/json" --data "{\"username\":\"John\", \"password\":\"8462927\", \"email\":\"johnd@email.com\"}"
# curl -XPUT http://127.0.0.1:5000/user -H "Content-Type:application/json" --data "{\"id\":\"1\", \"username\":\"John\", \"password\":\"202fjduy\", \"email\":\"johnd22@email.com\"}"
# curl -XGET http://127.0.0.1:5000/user/John

# curl -XPOST http://127.0.0.1:5000/events -H "Content-Type:application/json" --data "{\"name\":\"Movie night\", \"date\":\"2020-12-20\", \"description\":\"Popcorn\", \"author\":\"2\"}"
# curl -XPUT http://127.0.0.1:5000/events -H "Content-Type:application/json" --data "{\"id\":\"2\", \"name\":\"Movie night\", \"date\":\"2020-12-21\", \"description\":\"Popcorn(remember)\"}"
# curl -XGET http://127.0.0.1:5000/events
# curl -XGET http://127.0.0.1:5000/events/connectedEvents/2
