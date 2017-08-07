# coding:utf-8
import os.path
import json
from urllib import quote
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tornado.httpclient
import tornado.gen
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
    def task(self, url):
        import requests
        response = requests.get(url).content
        result, ex_meta = BtbookListParser.run(response)
        return result, ex_meta

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        word = self.get_argument('word')
        page = self.get_argument('page', default=None)
        ori_url = self.get_argument("url", default=None)
        if ori_url:
            url = ori_url
        else:
            if not page:
                print word
                url = u"http://www.btwhat.net/search/{}.html".format(word)
                print url
            else:
                url = u"http://www.btwhat.net/search/{}/2-{}.html".format(word, page)
        list_item, ex_meta = self.task(url)
        self.render('search_list.html',
                    title=word,
                    list_item=list_item,
                    pages=ex_meta["pages"])


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
