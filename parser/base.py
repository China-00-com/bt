# coding:utf-8

"""磁力链接实时"""

import re
import requests
from w3lib.encoding import html_to_unicode
from urlparse import urljoin
from urllib import unquote_plus, unquote
from bs4 import Tag, BeautifulSoup
from datetime import datetime, timedelta


class Item(object):
    def to_dict(self):
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d):
        self = cls()
        for k, v in d.items():
            self.__dict__[k] = v

    def show(self):
        for k, v in self.to_dict().items():
            print k, ":", v
        print "*" * 100


class ListItem(Item):
    def __init__(self):
        self.title = ""
        self.size = ""
        self.file_type = ""
        self.last_down = ""
        self.create_time = ""
        self.hot = 0
        self.contain = list()
        self.detail_url = ""


class DetailItem(Item):
    def __init__(self):
        self.title = ""
        self.file_type = ""
        self.file_size = ""
        self.create_time = ""
        self.hot_score = ""
        self.file_count = ""
        self.magnet_link = ""
        self.containt = ""


class HotWordItem(Item):
    def __init__(self):
        self.word = ""


class BaseParser(object):
    @classmethod
    def find_tag(cls, root, param):
        if not isinstance(root, (Tag, BeautifulSoup)):
            return None
        method = param.get("method", "find")
        params = param["params"]
        nth = param.get("nth", 0)
        if method == "find":
            tag = root.find(**params)
            return tag
        elif method == "find_all":
            tags = root.find_all(**params)
        elif method == "select":
            tags = root.select(**params)
        else:
            raise ValueError("param['method'] only support find, find_all and select")
        return tags[nth] if len(tags) > nth else None

    @classmethod
    def find_tags(cls, root, param):
        if not isinstance(root, (Tag, BeautifulSoup)):
            return []
        method = param.get("method", "find_all")
        params = param["params"]
        if method == "find":
            tag = root.find(**params)
            if tag is None:
                return []
            else:
                return [tag]
        elif method == "find_all":
            tags = root.find_all(**params)
        elif method == "select":
            tags = root.select(**params)
        else:
            raise ValueError("param['method'] only support find, find_all and select")
        return tags

    @classmethod
    def extract_tag_attribute(cls, root, name="text"):
        if root is None:
            return ""
        assert isinstance(root, (Tag, BeautifulSoup))
        if name == "text":
            return root.get_text().strip()
        else:
            value = root.get(name, "")
            if isinstance(value, (list, tuple)):
                return ",".join(value)
            else:
                return value.strip()

    @classmethod
    def find_extract_tag_attribute(cls, tag, params):
        if params.get("params"):
            tag = cls.find_tag(tag, params)
        attribute = params.get("attribute", "text")
        return cls.extract_tag_attribute(tag, attribute)

    @classmethod
    def get_soup(cls, document):
        soup = BeautifulSoup(document, "lxml")
        return soup

    @classmethod
    def get_tags(cls, soup):
        tags = soup.select(selector="div#wall > div.search-item")
        return tags


class HotWordParser(BaseParser):
    @classmethod
    def get_hot_words(cls, soup):
        pass

    def run(cls, **kwargs):
        pass


class ListParser(BaseParser):
    @classmethod
    def get_title(cls, soup):
        pass

    @classmethod
    def get_file_size(cls, soup):
        pass

    @classmethod
    def get_file_type(cls, soup):
        pass

    @classmethod
    def get_last_down(cls, soup):
        pass

    @classmethod
    def get_create_time(cls, soup):
        pass

    @classmethod
    def get_contain(cls, soup):
        pass

    @classmethod
    def get_detail_url(cls, soup):
        pass

    @classmethod
    def get_hot(cls, soup):
        pass

    @classmethod
    def get_pages(cls, soup):
        pass


class DetailParser(BaseParser):
    @classmethod
    def get_title(cls, soup):
        pass

    @classmethod
    def get_file_type(cls, soup):
        pass

    @classmethod
    def get_file_size(cls, soup):
        pass

    @classmethod
    def get_create_time(cls, soup):
        pass

    @classmethod
    def get_hot_score(cls, soup):
        pass

    @classmethod
    def get_file_count(cls, soup):
        pass

    @classmethod
    def get_magnet_link(cls, soup):
        pass

    @classmethod
    def get_contain(cls, soup):
        pass

    @classmethod
    def run(self, **kwargs):
        pass


if __name__ == "__main__":
    pass

"""
btbook
runbt.cc
cloudbt
https://github.com/a52948/cloudbt
"""
