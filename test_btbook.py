# coding:utf-8

import requests
from parser.btbook_parser import BtbookListParser

btbook_list_url = "http://www.btwhat.net/search/%E6%88%98%E7%A5%9E3/1-2.html"
list_document = requests.get(url=btbook_list_url).content

BtbookListParser.run(list_document)
