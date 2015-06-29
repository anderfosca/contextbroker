__author__ = 'anderson'
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from broker import broker

http_server = HTTPServer(WSGIContainer(broker))
http_server.listen(5000)
IOLoop.instance().start()