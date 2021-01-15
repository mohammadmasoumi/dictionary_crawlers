# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from dictionary_crawlers.dictionary_crawlers import processors


class LongManItem(scrapy.Item):
    # define the fields for your item here like:

    word = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    family_word = scrapy.Field(
        input_processor=processors.LongManFamilyWordProcessor()
    )
    header = scrapy.Field(
        input_processor=processors.LongManHeaderProcessor()
    )
