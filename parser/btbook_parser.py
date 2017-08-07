# coding:utf-8

import re
from urllib import urlencode,quote
from urlparse import unquote, urljoin
from parser.base import HotWordParser
from parser.base import ListParser
from parser.base import DetailParser
from parser.base import HotWordItem
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
    CONTAIN_SIZE = re.compile('span class="lightColor">(.*?)</span>')
    NUM_PAGE = {}
    PAGES = {"params": {"selector": "div.bottom-pager"}, "method": "select"}
    CURRENT = re.compile('<span>(\d+)</span>')
    HREF_NUM = re.compile('<a href="(.*?)">(\d+)</a>')
    FIELD_TEXT_RE = re.compile('decodeURIComponent\((.*?)\)')

    @classmethod
    def decode_field(cls, text):
        regex_result = cls.FIELD_TEXT_RE.findall(text)
        if not regex_result:
            field_text = text
        else:
            field_text = regex_result[0]
            print field_text
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
            text = cls.decode_field(str(tag))
            size = cls.CONTAIN_SIZE.findall(str(soup))[0]
            one = {
                "text": text,
                "size": size
            }
            con_list.append(one)
        return con_list

    @classmethod
    def get_detail_url(cls, soup):
        detail_url = cls.find_extract_tag_attribute(soup, cls.DETAIL_URL)
        detail_url = urljoin(cls.BASE_URL, detail_url)
        return detail_url

    @classmethod
    def get_pages(cls, soup):
        page_tag = cls.find_tag(soup, cls.PAGES)
        pages = list()
        papes_result = cls.HREF_NUM.findall(str(page_tag))
        for page in papes_result:
            list_url = urljoin(cls.BASE_URL, page[0])
            pages.append((int(page[1]), quote(list_url)))
        current = cls.CURRENT.findall(str(page_tag))[0]
        pages.append((int(current), "#"))
        pages = sorted(pages, key=lambda x: x[0])
        print pages
        return pages

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
            try:
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
            except:
                pass
        ex_meta = dict()
        ex_meta["pages"] = cls.get_pages(soup)
        return item_list, ex_meta


class BtbookDetailParser(DetailParser):
    FIELD_TEXT_RE = re.compile('decodeURIComponent\((.*?)\)')
    TITLE = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    FILE_TYPE = {"attribute": "text", "params": {"selector": "table.detail-table td:nth-of-type(1)"},
                 "method": "select"}
    CREATE_TIME = {"attribute": "text", "params": {"selector": "table.detail-table td:nth-of-type(2)"},
                   "method": "select"}
    HOT_SCORE = {"attribute": "text", "params": {"selector": "table.detail-table td:nth-of-type(3)"},
                 "method": "select"}
    FILE_SIZE = {"attribute": "text", "params": {"selector": "table.detail-table td:nth-of-type(4)"},
                 "method": "select"}
    FILE_COUNT = {"attribute": "text", "params": {"selector": "table.detail-table td:nth-of-type(5)"},
                  "method": "select"}
    MAGNET_LINK = re.compile(r'<a href="magnet.*?">(.*?)</a>')
    TAGS = {"attribute": "text", "params": {"selector": "h2"}, "method": "select"}
    CONTAIN = {"params": {"selector": "ol > li"}, "method": "select"}
    CONTAIN_SIZE = {"params": {"selector": "span"}, "method": "select"}

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
        hot_score = cls.find_extract_tag_attribute(soup, cls.HOT_SCORE)
        return hot_score

    @classmethod
    def get_file_count(cls, soup):
        file_count = cls.find_extract_tag_attribute(soup, cls.FILE_COUNT)
        return file_count

    @classmethod
    def get_magnet_link(cls, soup):
        magnet_link = cls.MAGNET_LINK.findall(str(soup))[0]
        return magnet_link

    @classmethod
    def get_contain(cls, soup):
        con_list = list()
        tags = cls.find_tags(soup, cls.CONTAIN)
        for tag in tags:
            text = cls.decode_field(str(tag))
            size = cls.find_extract_tag_attribute(tag, cls.CONTAIN_SIZE)
            one = {
                "text": text,
                "size": size
            }
            con_list.append(one)
        return con_list

    @classmethod
    def run(cls, document):
        soup = cls.get_soup(document)
        meta = DetailItem()
        meta.title = cls.get_title(soup)
        meta.file_type = cls.get_file_type(soup)
        meta.create_time = cls.get_create_time(soup)
        meta.hot_score = cls.get_hot_score(soup)
        meta.file_size = cls.get_file_size(soup)
        meta.file_count = cls.get_file_count(soup)
        meta.magnet_link = cls.get_magnet_link(soup)
        meta.containt = cls.get_contain(soup)
        return meta


class BtbookHotWordParser(HotWordParser):
    @classmethod
    def get_hot_words(cls, soup):
        hot_words = list()
        return hot_words

    @classmethod
    def run(cls, document):
        soup = cls.get_soup(document)
        hot_words = cls.get_hot_words(soup)
        return hot_words
