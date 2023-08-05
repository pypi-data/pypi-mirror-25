# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/22
import threading
from time import sleep

from hunters.utils import ForeverThreadPool

fx = ForeverThreadPool(10)


def test():
    print("MyPrint->" + threading.currentThread().name)
    sleep(1)
    raise Exception("Oh NO")


fx.submit(target=test, args=())
print("Hello")
