import sys

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from model_monitor import app

if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    port = 8000

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port, address="0.0.0.0")
IOLoop.instance().start()
