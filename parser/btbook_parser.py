# coding:utf-8

import re
from urlparse import unquote
from parser.base import ListParser
from parser.base import DetailParser
from parser.base import ListItem
from parser.base import DetailItem


class BtbookListParser(ListParser):
    TITLE = {"params": {"selector": "div.item-title > h3"}, "method": "select"}
    CONTAIN = {"params": {"selector": "div.item-list > ul > li"}, "method": "select"}
    FILE_TYPE = {"params": {"selector": "div.item-list > ul > li"}, "method": "select"}
    FILE_SIZE = {"params": {"selector": "div.item-list > ul > li"}, "method": "select"}
    LAST_DOWN = {"params": {"selector": "div.item-list > ul > li"}, "method": "select"}
    TIME = {}

    @classmethod
    def decode_field(cls, text):
        field_text_re = re.compile('decodeURIComponent\((.*?)\);')
        regex_result = field_text_re.findall(text)
        if not regex_result:
            field_text = text
        else:
            field_text = regex_result[0]
            field_text = "".join(map(lambda x: x.strip('"'), field_text.split("+")))
            field_text = unquote(field_text)
        return field_text

    @classmethod
    def get_title(cls, soup):
        title = cls.find_extract_tag_attribute(soup, cls.TITLE)
        return title

    @classmethod
    def get_file_size(cls, soup):
        file_size = cls.find_extract_tag_attribute(soup, cls.FILE_SIZE)
        return file_size

    @classmethod
    def get_file_type(cls, soup):
        file_type = cls.find_extract_tag_attribute(soup, cls.FILE_TYPE)
        return file_type

    @classmethod
    def get_last_down(cls, soup):
        last_down = cls.find_extract_tag_attribute(soup, cls.LAST_DOWN)
        return last_down

    @classmethod
    def get_time(cls, soup):
        time = cls.find_extract_tag_attribute(soup, cls.TIME)
        return time

    @classmethod
    def get_contain(cls, soup):
        contain = cls.find_extract_tag_attribute(soup, cls.CONTAIN)
        return contain

    @classmethod
    def get_detail_url(cls, soup):
        detail_url = cls.find_extract_tag_attribute(soup, cls.CONTAIN)
        return detail_url

    def run(self, document):
        item_list = list()
        soup = self.get_soup(document)
        tags = self.get_tags(soup)
        for tag in tags:
            one_item = ListItem()
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
