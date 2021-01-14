# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from .processors import FamilyWordProcessor, HeaderProcessor


class DictionaryCrawlersItem(scrapy.Item):
    # define the fields for your item here like:

    word = scrapy.Field()
    family_word = scrapy.Field(
        input_processor=FamilyWordProcessor()
    )
    header = scrapy.Field(
        input_processor=HeaderProcessor()
    )