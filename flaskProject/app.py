#http://127.0.0.1:5000/api/v1/hello-world-10

from flask import Flask
from wsgiref.simple_server import make_server

app = Flask(__name__)


@app.route('/api/v1/hello-world-10')
def hello_world():
    return 'Hello World! 10'


if __name__ == '__main__':
    app.run()

server = make_server('', 5000, app)
server.serve_forever()