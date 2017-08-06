# coding:utf-8

import re
from urlparse import unquote, urljoin
from parser.base import ListParser
from parser.base import DetailParser
from parser.base import ListItem
from parser.base import DetailItem


class BtbookListParser(ListParser):
    BASE_URL = "http://www.btwhat.net"
    TITLE = {"params": {"selector": "div.item-title > h3 > a"}, "method": "select"}
    FILE_TYPE = re.compile('fileType.">(.*?)</span>')
    FILE_SIZE = {"params": {"selector": "b.yellow-pill"}, "method": "select"}
    LAST_DOWN = re.compile('<span>Last Download：<b>(.*?)</b></span>')
    CREATE_TIME = re.compile('Create Time：.*?<b>(.*?)</b>', re.S)
    HOT = re.compile('<span>Hot：<b>(.*?)</b></span>')
    DETAIL_URL = {"attribute": "href", "params": {"selector": "div.item-title > h3 > a"}, "method": "select"}

    CONTAIN = {"params": {"selector": "div.item-list > ul > li"}, "method": "select"}
    NUM_PAGE = {}
    FIELD_TEXT_RE = re.compile('decodeURIComponent\((.*?)\)')

    @classmethod
    def decode_field(cls, text):
        regex_result = cls.FIELD_TEXT_RE.findall(text)
        if not regex_result:
            field_text = text
        else:
            field_text = regex_result[0]
            field_text = eval(field_text)
            field_text = unquote(field_text)
        return field_text

    @classmethod
    def get_title(cls, soup):
        title = cls.find_extract_tag_attribute(soup, cls.TITLE)
        title = cls.decode_field(title)
        return title

    @classmethod
    def get_file_size(cls, soup):
        file_size = cls.find_extract_tag_attribute(soup, cls.FILE_SIZE)
        file_size = cls.decode_field(file_size)
        return file_size

    @classmethod
    def get_file_type(cls, soup):
        file_type = cls.FILE_TYPE.findall(str(soup))[0]
        return file_type

    @classmethod
    def get_last_down(cls, soup):
        last_down = cls.LAST_DOWN.findall(str(soup))[0]
        return last_down

    @classmethod
    def get_create_time(cls, soup):
        time = cls.CREATE_TIME.findall(str(soup))[0]
        return time

    @classmethod
    def get_hot(cls, soup):
        hot = cls.HOT.findall(str(soup))[0]
        return int(hot)

    @classmethod
    def get_contain(cls, soup):
        con_list = list()
        tags = cls.find_tags(soup, cls.CONTAIN)
        for tag in tags:
            one = cls.decode_field(str(tag))
            con_list.append(one)
        return con_list

    @classmethod
    def get_detail_url(cls, soup):
        detail_url = cls.find_extract_tag_attribute(soup, cls.DETAIL_URL)
        detail_url = urljoin(cls.BASE_URL, detail_url)
        return detail_url

    @classmethod
    def get_tags(cls, soup):
        tags = soup.select(selector="div#wall > div.search-item")
        return tags

    @classmethod
    def run(cls, document):
        item_list = list()
        soup = cls.get_soup(document)
        tags = cls.get_tags(soup)
        for tag in tags:
            one_item = ListItem()
            one_item.title = cls.get_title(tag)
            one_item.file_type = cls.get_file_type(tag)
            one_item.size = cls.get_file_size(tag)
            one_item.last_down = cls.get_last_down(tag)
            one_item.create_time = cls.get_create_time(tag)
            one_item.hot = cls.get_hot(tag)
            one_item.detail_url = cls.get_detail_url(tag)
            one_item.contain = cls.get_contain(tag)
            item_list.append(one_item)
        return item_list


class BtbookDetailParser(DetailParser):
    TITLE = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    FILE_TYPE = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    FILE_SIZE = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    CREATE_TIME = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    HOT_STROE = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    FILE_COUNT = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    MAGNET_LINK = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    TAGS = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    CONTAINT = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}

    @classmethod
    def get_title(cls, soup):
        title = cls.find_extract_tag_attribute(soup, cls.TITLE)
        return title

    @classmethod
    def get_mtags(cls, soup):
        tags = cls.find_extract_tag_attribute(soup, cls.TAGS)
        return tags

    @classmethod
    def get_file_type(cls, soup):
        file_type = cls.find_extract_tag_attribute(soup, cls.FILE_TYPE)
        return file_type

    @classmethod
    def get_file_size(cls, soup):
        file_size = cls.find_extract_tag_attribute(soup, cls.FILE_SIZE)
        return file_size

    @classmethod
    def get_create_time(cls, soup):
        create_time = cls.find_extract_tag_attribute(soup, cls.CREATE_TIME)
        return create_time

    @classmethod
    def get_hot_score(cls, soup):
        hot_score = cls.find_extract_tag_attribute(soup, cls.HOT_STROE)
        return hot_score

    @classmethod
    def get_file_count(cls, soup):
        file_count = cls.find_extract_tag_attribute(soup, cls.FILE_COUNT)
        return file_count

    @classmethod
    def get_magnet_link(cls, soup):
        magnet_link = cls.find_extract_tag_attribute(soup, cls.MAGNET_LINK)
        return magnet_link

    @classmethod
    def get_contain(cls, soup):
        contain = cls.find_extract_tag_attribute(soup, cls.CONTAINT)
        return contain

    @classmethod
    def run(self, document):
        soup = self.get_soup(document)
        meta = DetailItem()
        return meta
