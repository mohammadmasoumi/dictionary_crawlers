#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

import re
from collections import defaultdict
from logging import getLogger

from itemloaders.processors import TakeFirst

logger = getLogger(__name__)

__all__ = (
    "FamilyWordProcessor",
    "HeaderProcessor",
    "default_input_processor",
    "default_output_processor"
)

default_input_processor = TakeFirst()
default_output_processor = TakeFirst()


class FamilyWordProcessor:

    def __call__(self, iterable, **kwargs):
        """
        :param iterable: xpath query result
        :param kwargs: scrapy context
        :return: a dict which contains family words
        """

        word_family = defaultdict(list)

        # current part of speech
        current_pos = None

        for item in iterable:
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                part_of_speech = re.search(r'\((.*?)\)', iterable_item)

                if part_of_speech:
                    try:
                        current_pos = part_of_speech.group(1)
                    except Exception as exc:
                        logger.exception(exc)

                elif current_pos:
                    word_family[current_pos].append(iterable_item)

        return dict(word_family)


class HeaderProcessor:

    def __call__(self, iterable, **kwargs):
        """
        :param iterable: xpath query result
        :param kwargs: scrapy context
        :return:
        """

        headers = defaultdict(dict)

        # current part of speech
        current_pos = None
        logger.debug("######################################################")
        for item in iterable:
            item.xpath("//span[contains(@class, 'HWD')]//text()")
            # logger.info(f"item: {item}")
            logger.info("-------------------------------------------------------------")
            # iterable_item = item.strip() if isinstance(item, str) else None
            #
            # if iterable_item:
            #     part_of_speech = re.search(r'\((.*?)\)', iterable_item)
            #     if part_of_speech:
            #         try:
            #             current_pos = part_of_speech.group(1)
            #         except Exception as exc:
            #             logger.exception(exc)
            #
            #     elif current_pos:
            #         headers[current_pos].append(iterable_item)

        logger.debug("######################################################")

        return dict(headers)
