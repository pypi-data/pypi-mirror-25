# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/4
import datetime
import hashlib
import html
import logging
import re
import threading
import urllib
from time import sleep
from urllib.parse import urljoin

from lxml.html import fromstring

from hunters.constant import Regex

logger = logging.getLogger("hunters.util")


def decode_html(input):
    s = html.unescape(input)
    return s


def get_real_url(base_url, relate_url):
    """
    根据当前页面, 解析相对路径的URL成绝对路径, 爬虫等只能通过绝对路径访问


    http://baidu.com/a/b/c.html  --> ../../m.html

    ==> http://baidu.com/a/m.html

    :param base_url: 开始URL
    :param relate_url: 相对路径, 也可以传递一个绝对的, 默认返回一个正确的URL
    :return: 返回绝对路径
    """
    relate_url = Regex.RE_URL_COMMENT.sub("", relate_url.strip())
    if len(relate_url) == 0:
        return base_url

    if relate_url.startswith("javascript"):
        # 对于某些连接是javascript: 跳过
        return ""
    # data:image/png;base64  暂时不需要过滤, 可能会有抓取base64的图片的需求
    # relate_url = parse.unquote(decode_html(relate_url))
    # relate_url = parse.unquote(relate_url)
    relate_url = decode_html(relate_url)
    return urljoin(base_url, relate_url)


def dom(html):
    """ dom 化一个html文档, 以便能够使用cssselect选择器"""
    return fromstring(html)


def mtime():
    return datetime.datetime.now().microsecond


def md5hex(str_data):
    """ md5 hex"""
    hash_ = hashlib.md5()
    hash_.update(str_data.encode('utf-8'))
    return hash_.hexdigest()


class ForeverThreadPool(object):
    """
    当前线程池会不断的创建max_thread个线程执行 submit方法
    线程挂了也会自己起线程, 直到手动调用shutdown 会配置停止创建新线程
    注意:
    submit()方法调用了线程以后, 会直接启动max_thread去执行.
    """

    def __init__(self, max_thread):
        self._max_thread = max_thread
        self._thread_pool = {}
        self._stop_all = False

    def shutdown(self):
        self._stop_all = True

    def submit(self, target, args):
        threading.Thread(target=self._submit, args=(target, args)).start()

    def _submit(self, target, args):

        def exception_wrap():
            try:
                target(*args)
            except Exception as e:
                logger.error("Thread Die [%s] %s" % (threading.currentThread().name, e))
                logger.exception(e)
                self._thread_pool.pop(threading.currentThread().name)

        while True:

            pending = []

            num_pending = self._max_thread - len(self._thread_pool.keys())

            for i in range(num_pending):
                t = threading.Thread(target=exception_wrap, args=())
                self._thread_pool[t.name] = t
                pending.append(t)

            for t in pending:
                logger.info("Main[%s] START worker[%s]" % (threading.current_thread().name, t.name))
                t.start()

            if self._stop_all:  #: 如果接收到停止信号, 退出循环
                break

            sleep(0.01)

        for t in self._thread_pool.values():
            t.join()  #: 等待所有子线程退出


if "__main__" == __name__:
    url = get_real_url("http://www.baidu.com", "/about.html#areas")
    print(url)
    url = "http://www.so.com:80/s?ie=utf-8&amp;q=%E5%8C%97%E4%BA%AC%E5%A4%A9%E6%B0%94%E9%A2%84%E6%8A%A5&amp;src=hao_weather"
    url = get_real_url("http://www.baidu.com", url)
    print(url)
    print(decode_html("\x64\x6f\x63\x75\x6d\x65\x6e\x74"))
    print(dom("<a>mm</a>").cssselect('a')[0].text)
