#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

from .base import BaseSpider


class LongmanDictionarySpider(BaseSpider):
    name = 'longman'
    allowed_domains = ["ldoceonline.com"]
    base_url = 'https://www.ldoceonline.com/dictionary/'
    item_loader_xpath = {
        'family_word': "//div[@class='wordfams']//text()",
        'header': {
            'parent': "//span[contains(@class, 'Head')]",
            'children': {
                'hwd':"//span[contains(@class, 'HWD')]"
            }
        },
    }