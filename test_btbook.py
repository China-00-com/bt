# coding:utf-8

import requests
from parser.btbook_parser import BtbookListParser
from parser.btbook_parser import BtbookDetailParser


def test_list():
    btbook_list_url = "http://www.btwhat.net/search/%E6%88%98%E7%A5%9E3/1-2.html"
    list_document = requests.get(url=btbook_list_url).content
    result, ex_meta = BtbookListParser.run(list_document)
    for i in result:
        i.show()
    for i in ex_meta.items():
        print i


def test_detail():
    one_detail_url = "http://www.btwhat.net/wiki/f574ba521d2a9b784d470c91108f6b8a4b4a2dc9.html"
    detail_document = requests.get(url=one_detail_url).content
    detail = BtbookDetailParser.run(detail_document)
    detail.show()


test_detail()
