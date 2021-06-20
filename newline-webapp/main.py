from tornado.wsgi import WSGIContainer
from tornado import web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from webapp import app
from tornado.log import enable_pretty_logging
enable_pretty_logging()

class MainHandler(web.RequestHandler):

    def prepare(self):
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host, permanent=False)

    def get(self):
        self.write("Hello, world")



ssl_details = {"certfile": "/newline-webapp/ssl/cert.pem", "keyfile": "/newline-webapp/ssl/key.pem"}
application = web.Application([(r'/', MainHandler)])
application.listen(80)
http_server = HTTPServer(WSGIContainer(app), ssl_options=ssl_details)
http_server.listen(443)
IOLoop.instance().start()
