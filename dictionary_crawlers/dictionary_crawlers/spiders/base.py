#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

from logging import getLogger

import scrapy
from scrapy.loader import ItemLoader

from ..items import DictionaryCrawlersItem
from ..processors import default_input_processor, default_output_processor

logger = getLogger(__name__)


class BaseSpider(scrapy.Spider):
    name = None
    base_url = None
    item_loader_xpath = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        assert self.base_url is not None, "`base_url` is required!"
        assert self.item_loader_xpath is not None, "`item_loader_xpath` is required!"

        # initialize variables
        self.start_urls = tuple(self.base_url + word for word in kwargs.values())
        name = self.__class__.__name__ if self.name is None else self.name

        super(BaseSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        """
        :return:
        """
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response, **kwargs):
        """
        response.xpath("//span[contains(@class, 'Head')]//text()").getall()
        :param response:
        :param kwargs:
        :return:
        """
        item_loader = ItemLoader(item=DictionaryCrawlersItem(), response=response, spider_name=self.name)
        item_loader.default_input_processor = default_input_processor
        item_loader.default_output_processor = default_output_processor

        # logger.info("************************************** TEST **************************************")
        # logger.info("**********************************************************************************")
        # for section in response.xpath("//span[contains(@class, 'Head')]").getall():
        #     logger.info(section.split())
        # logger.info("**********************************************************************************")
        # logger.info("**********************************************************************************")

        for field_name, xpath in self.item_loader_xpath.items():
            item_loader.add_xpath(field_name=field_name, xpath=xpath)

        item_loader.add_value('word', response.request.url.split("/")[-1])

        yield item_loader.load_item()
