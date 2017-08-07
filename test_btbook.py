# coding:utf-8

import requests
from parser.btbook_parser import BtbookListParser
from parser.btbook_parser import BtbookDetailParser
from parser.cilisoba_parser import CilisobaListParser
from parser.cilisoba_parser import CilisobaDetailParser


ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

def test_list(url, parser):
    btbook_list_url = url
    list_document = requests.get(url=btbook_list_url).content
    result, ex_meta = parser.run(list_document)
    for i in result:
        i.show()
    for i in ex_meta.items():
        print i


def test_detail(url, parser):
    one_detail_url = url
    detail_document = requests.get(url=one_detail_url,headers={"user-agent":ua}).content
    detail = parser.run(detail_document)
    detail.show()


url = "http://www.cilisoba.net/h/33795336"
parser = CilisobaDetailParser
test_detail(url, parser)
