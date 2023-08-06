#!/usr/bin/python3

import threading
import socket

from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, StaticFileHandler, Application, url
import os

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
except:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


########################################################################
class Clients(dict):
    """"""

    ##----------------------------------------------------------------------
    #def shell(self, client):
        #""""""
        #return self[client][1]


    #----------------------------------------------------------------------
    def client(self, client):
        """"""
        return self[client][0]


    #----------------------------------------------------------------------
    def write_message(self, client, message):
        """"""
        self.client(client).write_message(message)


clients = Clients()


#########################################################################
#class HomeHandler(RequestHandler):
    #""""""

    #def get(self):
        #""""""
        #self.render("html/index.html")


#########################################################################
#class PrivacyHandler(RequestHandler):
    #""""""

    #def get(self):
        #""""""
        #self.render("html/privacy.html")


########################################################################
class WSHandler(WebSocketHandler):
    """"""

    #----------------------------------------------------------------------
    def check_origin(self, origin):
        """"""
        return True


    #----------------------------------------------------------------------
    def open(self):
        """"""
        self.print_log('tornado_ok')


    #----------------------------------------------------------------------
    def on_close(self):
        """"""
        if hasattr(self, 'user_hash'):
            print("connection closed: {}".format(self.user_hash))
            #if DEBUG:
            clients.pop(self.user_hash)


    #----------------------------------------------------------------------
    def print_log(self, message):
        """"""
        #print(message)
        self.write_message({'type': 'log', 'message': message})


    #----------------------------------------------------------------------
    def on_message(self, message):
        """"""
        msg = message.split(';', 3)  #3 is max args (used in piton_open)

        if hasattr(self, 'user_hash'):
            self.t(self.user_hash, msg[0], msg[1:]).start()
        else:
            self.piton_register(msg[1])
            #self.a = threading.Thread(target=self.piton_register, args=(msg[1], ))
            #self.a.start()


    #----------------------------------------------------------------------
    def piton_register(self, user_hash):
        """"""
        if user_hash in clients.keys():
            self.print_log("User already registered.")
            return

        clients[user_hash] = [self]
        self.user_hash = user_hash

        self.t = lambda u_hash, fn, args:threading.Thread(target=getattr(self, 'piton_{}'.format(fn)), args=(u_hash, *args))
        self.print_log("Registration successful {}".format(user_hash))
        #if DEBUG:
        print("Registration successful {}".format(user_hash))



    #----------------------------------------------------------------------
    @classmethod
    def piton_interprete(cls, user_hash, id_, code):
        """"""



    #----------------------------------------------------------------------
    @classmethod
    def piton_gpio(cls, user_hash, cmd, *args):
        """"""

        if cmd == 'output':
            pin, state = args
            command = "GPIO.setup({}, GPIO.OUT, {})".format(*args)

        eval(command)





########################################################################
class ImageHandler(RequestHandler):

    #----------------------------------------------------------------------
    def set_default_headers(self):

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    #----------------------------------------------------------------------
    def get(self):
        """"""
        user= self.request.arguments['user'][0].decode('utf-8')
        id_= self.request.arguments['id'][0].decode('utf-8')
        #shell = clients.shell(user)
        #self.write(shell.get_plot(id_))


    #----------------------------------------------------------------------
    def options(self):
        """"""
        self.set_status()
        self.finish()





#----------------------------------------------------------------------
def make_app():


    settings = {
        "debug": True,
        "static_path": os.path.join(os.path.dirname(__file__), "html"),
        #"static_path": os.path.join(os.path.dirname(raspn.__file__), 'html'),

        'static_url_prefix': '/resources/',

        "xsrf_cookies": False,
    }


    return Application([
        #url(r'^/$', HomeHandler),
        #url(r'^/privacy$', PrivacyHandler),
        url(r'^/image.jpeg', ImageHandler),
        #url(r'^/animation.mp4', AnimationHandler),
        url(r'^/ws', WSHandler),
    ], **settings)




#----------------------------------------------------------------------
def run():
    """"""
    port = 8888

    print("Raspmanager running on port {}".format(port))
    application = make_app()
    http_server = HTTPServer(application)
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == '__main__':
    run()
