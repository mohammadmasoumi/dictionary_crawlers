# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from logging import getLogger

logger = getLogger(__name__)


class DictionaryCrawlersPipeline:
    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        # logger.debug("******************* PIPELINE *******************")
        # logger.debug("************************************************")
        # for key, value in item.items():
        #     logger.debug(f"key: {key}, value {value}")
        # logger.debug("************************************************")
        # logger.debug("************************************************")

        return item
