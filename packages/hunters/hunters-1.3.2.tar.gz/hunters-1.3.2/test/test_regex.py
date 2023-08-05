# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/11
import re

url = "http://www.baidu.com/da.js?xxxxxxxx"
clean_url = re.sub(r"\?.*", "", url)
print(clean_url, url)
