#coding:utf-8
#--coding:utf-8
import os
import tornado.web
from Handers import *
settings = {
    "debug": False
}
if __name__ == '__main__':
    # tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/tags", TagHander),
            (r"/girls",PicHander)
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static").replace("\\","/"),
        template_path = os.path.join(os.path.dirname(__file__), ""),
        debug = True
        )
    print(os.path.join(os.path.dirname(__file__), "static").replace("\\","/"))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8889)
    tornado.ioloop.IOLoop.current().start()