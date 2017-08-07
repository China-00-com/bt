# coding:utf-8
import os.path
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from parser.btbook_parser import BtbookListParser
from parser.btbook_parser import BtbookDetailParser



define("port", default=8081, help="run on the given port", type=int)


class GetHotHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    title="磁力云（ciliyun.net）")


class SearchListHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word')
        BtbookListParser.run(word=word)
        self.render('search_list.html',
                    title=word,)


class SearchDetailHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("search_detail.html",
                    title="详情")


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/search', SearchListHandler),
            (r'/detail', SearchDetailHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
