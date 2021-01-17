#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

from ..items import LongManItem
from .base import BaseSpider


class LongmanDictionarySpider(BaseSpider):
    name = 'longman'
    allowed_domains = ["ldoceonline.com"]
    base_url = 'https://www.ldoceonline.com/dictionary/'
    item_loader_cls = LongManItem()
    item_loader_xpath = {
        'family_word': "//div[@class='wordfams']//text()",
        'ldocs': "//span[@class='dictentry']"
    }
