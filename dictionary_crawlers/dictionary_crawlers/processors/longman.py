#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et
# flake8: noqa

import logging
import re
from collections import defaultdict

from lxml import etree

logger = logging.getLogger(__name__)

__all__ = (
    'LongManFamilyWordProcessor',
    'LongManHeaderProcessor'
)


class LongManFamilyWordProcessor:

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


class LongManHeaderProcessor:
    # _HEADER_MAPPING = {
    #     "hwd": "<span class=\"HWD\">(?:\s)*([^<}]+)</span>",
    #     "hyphenation": "<span class=\"HYPHENATION\">(?:\s)*([^<}]+)</span>",
    #     "homnum": "<span class=\"HOMNUM\">(?:\s)*([^<}]+)</span>",
    #     "pos": "<span class=\"POS\">(?:\s)*([^<}]+)</span>",
    #     "british_pron": "<span data-src-mp3=\"(?:\s)*([^<}]+)\" class=\"speaker brefile fas fa-volume-up hideOnAmp\"",
    #     "american_pron": "<span data-src-mp3=\"(?:\s)*([^<}]+)\" class=\"speaker amefile fas fa-volume-up hideOnAmp\"",
    # }  # NOQA

    _HEADER_XPATH_MAPPING = {
        'hwd': "//span[@class='HWD']//text()",
        'hyphenation': "//span[@class='HYPHENATION']//text()",
        'homnum': "//span[@class='HOMNUM']//text()",
        'pos': "//span[@class='POS']//text()",
        'british_pron': "//span[contains(@class, 'brefile')]/@data-src-mp3",
        'american_pron': "//span[contains(@class, 'amefile')]/@data-src-mp3",
    }

    @staticmethod
    def _filter_definition(defs: list):
        """

        :param defs:
        :return:
        """

        return ''.join(filter(lambda x: not x.startswith('\\'), defs))

    def __call__(self, iterable, **kwargs):
        """
        :param iterable: xpath query result
        :param kwargs: scrapy context
        :return:
        """
        definitions = {}

        logger.debug("######################################################")
        for item in iterable:
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                html = etree.HTML(iterable_item)

                # header
                header = {}
                for key, xpath in self._HEADER_XPATH_MAPPING.items():
                    value = html.xpath(xpath)
                    # logger.debug(f"{key}: {value}")
                    header.update({key: value[-1]}) if value else None

                if header:
                    definitions[header.get('homnum')] = header

                # definition
                for sense in html.xpath("//span[@class='Sense']"):
                    # logger.debug(etree.tostring(sense))
                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    sense_num = sense.xpath("span[1]//text()")
                    sign_post = sense.xpath("span[@class='SIGNPOST']//text()")
                    gram = sense.xpath("span[@class='GRAM']//text()")

                    logger.debug(f"sense_num: {sense_num}")
                    logger.debug(f"sign_post: {sign_post}")
                    logger.debug(f"gram: {gram}")

                    for sub_sense in sense.xpath("//span[@class='Subsense']"):
                        sub_sense_num = sub_sense.xpath("span[1]//text()")
                        active = sub_sense.xpath("span[@class='ACTIV']//text()")
                        main_definition = self._filter_definition(sub_sense.xpath("span[@class='DEF']//text()"))

                        logger.debug(f"sub_sense_num: {sub_sense_num}")
                        logger.debug(f"active: {active}")
                        logger.debug(f"main_definition: {main_definition}")

                        for example in sub_sense.xpath("span[@class='EXAMPLE']"):
                            example_text = self._filter_definition(example.xpath("text()"))
                            example_audio = example.xpath("@data-src-mp3")

                            logger.debug(f"example_text: {example_text}")
                            logger.debug(f"example_audio: {example_audio}")

                        for collocation_example in sub_sense.xpath("span[@class='ColloExa']"):
                            collocation_text = self._filter_definition(collocation_example.xpath("span[1]//text()"))
                            collocation_audio = collocation_example.xpath("span[2]//@data-src-mp3")

                            logger.debug(f"collocation_text: {collocation_text}")
                            logger.debug(f"collocation_audio: {collocation_audio}")

                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        logger.debug("######################################################")
        return dict(definitions)
