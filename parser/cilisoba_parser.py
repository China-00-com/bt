# coding:utf-8

"""cilisoba.net"""

import requests
import re
from urlparse import unquote, urljoin
from parser.base import ListParser
from parser.base import DetailParser
from parser.base import ListItem
from parser.base import DetailItem


class CilisobaListParser(ListParser):
    BASE_URL = "http://www.cilisoba.net"
    TITLE = {"params": {"selector": "a.title"}, "method": "select"}
    FILE_SIZE = re.compile('Total size:(.*?)Total requests')
    LAST_DOWN = re.compile('Last access time:(.*?)<', re.S)
    CREATE_TIME = {"params": {"selector": "span.ctime"}, "method": "select"}
    HOT = re.compile('Total requests:(.*?)Last')
    DETAIL_URL = {"attribute": "href", "params": {"selector": "a.title"}, "method": "select"}
    CONTAIN = {"params": {"selector": "div.files > ul > li"}, "method": "select"}

    NUM_PAGE = {}
    PAGES = {"params": {"selector": "ul.pagination"}, "method": "select"}
    HREF_NUM = re.compile('<li class="(.*?)"><a href="(.*?)"> (\d+) <')

    @classmethod
    def get_title(cls, soup):
        title = cls.find_extract_tag_attribute(soup, cls.TITLE)
        return title

    @classmethod
    def get_file_size(cls, soup):
        file_size = cls.FILE_SIZE.findall(str(soup))[0]
        return file_size

    @classmethod
    def get_file_type(cls, soup):
        return "unknown"

    @classmethod
    def get_last_down(cls, soup):
        last_down = cls.LAST_DOWN.findall(str(soup))[0]
        return last_down

    @classmethod
    def get_create_time(cls, soup):
        time = cls.find_extract_tag_attribute(soup, cls.CREATE_TIME)
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
            con = str(tag)
            if "<li>....</li>" in con:
                continue
            con = con.strip("<li>").strip("</li>").split(" ")
            text = con[0]
            size = "".join(con[1:])
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
        pages = dict()
        papes_result = cls.HREF_NUM.findall(str(page_tag))
        for page in papes_result:
            if page[0] == "active":
                pages[page[2]] = "#"
            else:
                pages[page[2]] = urljoin(cls.BASE_URL, page[1])
        return pages

    @classmethod
    def get_tags(cls, soup):
        tags = soup.select(selector="td.x-item")
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
        ex_meta = dict()
        ex_meta["pages"] = cls.get_pages(soup)
        return item_list, ex_meta


class CilisobaDetailParser(DetailParser):
    TITLE = {"attribute": "text", "params": {"selector": "div.container h4:nth-of-type(1)"}, "method": "select"}
    CREATE_TIME = re.compile('Creation Time</th>.*?<td>(.*?)</td>', re.S)
    HOT_SCORE = re.compile('Total Requests</th>.*?<td>(.*?)</td>', re.S)
    FILE_SIZE = re.compile('File Size</th>.*?<td>(.*?)</td>', re.S)
    FILE_COUNT = re.compile('Total Files</th>.*?<td>(.*?)</td>', re.S)
    MAGNET_LINK = re.compile(r'<a href="magnet.*?">(.*?)</a>')
    CONTAIN = {"params": {"selector": "div.files > ul > li"}, "method": "select"}
    CONTAIN_SIZE = {"params": {"selector": "span"}, "method": "select"}

    @classmethod
    def get_title(cls, soup):
        title = cls.find_extract_tag_attribute(soup, cls.TITLE)
        return title

    @classmethod
    def get_file_type(cls, soup):
        return "UNKNOWN"

    @classmethod
    def get_file_size(cls, soup):
        file_size = cls.FILE_SIZE.findall(str(soup))[0]
        return file_size

    @classmethod
    def get_create_time(cls, soup):
        create_time = cls.CREATE_TIME.findall(str(soup))[0]
        return create_time

    @classmethod
    def get_hot_score(cls, soup):
        hot_score = cls.HOT_SCORE.findall(str(soup))[0]
        return hot_score

    @classmethod
    def get_file_count(cls, soup):
        file_count = cls.FILE_COUNT.findall(str(soup))[0]
        return file_count

    @classmethod
    def get_magnet_link(cls, hash_code):
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        magnet = "http://www.cilisoba.net/api/json_info?hashes=%s" % hash_code
        magnet = requests.get(url=magnet,headers={"user-agent":ua}).json()["info_hash"]
        magnet_link = "magnet:?xt=urn:btih:" + magnet
        return magnet_link

    @classmethod
    def get_contain(cls, soup):
        con_list = list()
        tags = cls.find_tags(soup, cls.CONTAIN)
        for tag in tags:
            con = str(tag).split()
            text = con[0]
            size = "".join(con[1:])
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
