from flask import Flask
from gevent.pywsgi import WSGIServer
from yourapplication import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
app = Flask(__name__)


@app.route('/api/v1/hello-world-10')
def hello_world():
    return 'Hello World! {10}'


if __name__ == '__main__':
    app.run()
