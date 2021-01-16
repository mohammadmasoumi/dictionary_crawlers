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
                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    sense_num = self._filter_definition(sense.xpath("span[1]//text()"))
                    sign_post = self._filter_definition(sense.xpath("span[@class='SIGNPOST']//text()"))
                    gram = self._filter_definition(sense.xpath("span[@class='GRAM']//text()"))

                    logger.debug(f"sense_num: {sense_num}")
                    logger.debug(f"sign_post: {sign_post}")
                    logger.debug(f"gram: {gram}")

                    # cross refs
                    for cross_ref in sense.xpath("span[@class='Crossref']//a"):
                        cross_ref_title = self._filter_definition(cross_ref.xpath("@title"))
                        cross_ref_link = self._ref_link(cross_ref.xpath("@href"))

                        logger.debug(f"cross_ref_title: {cross_ref_title}")
                        logger.debug(f"cross_ref_link: {cross_ref_link}")

                    for example in sense.xpath("span[@class='EXAMPLE']"):
                        example_text = self._filter_definition(example.xpath("text()"))
                        example_audio = example.xpath("span[1]//@data-src-mp3")

                        logger.debug(f"example_text: {example_text}")
                        logger.debug(f"example_audio: {example_audio}")

                    for collocation_example in sense.xpath("span[@class='ColloExa']"):
                        collocation_text = self._filter_definition(collocation_example.xpath("span[1]//text()"))
                        collocation_audio = collocation_example.xpath("span[2]//@data-src-mp3")

                        logger.debug(f"collocation_text: {collocation_text}")
                        logger.debug(f"collocation_audio: {collocation_audio}")

                    for grammar_example in sense.xpath("span[@class='GramExa']"):
                        grammar_text = self._filter_definition(grammar_example.xpath("span[1]//text()"))
                        grammar_audio = grammar_example.xpath("span[2]//@data-src-mp3")

                        logger.debug(f"grammar_text: {grammar_text}")
                        logger.debug(f"grammar_audio: {grammar_audio}")

                    for sub_sense in sense.xpath("span[@class='Subsense']"):
                        sub_sense_num = self._filter_definition(sub_sense.xpath("span[1]//text()"))
                        active = self._filter_definition(sub_sense.xpath("span[@class='ACTIV']//text()"))
                        geo = self._filter_definition(sub_sense.xpath("span[@class='GEO']//text()"))
                        syn = self._filter_definition(sub_sense.xpath("span[@class='SYN']//text()"))
                        main_definition = self._filter_definition(sub_sense.xpath("span[@class='DEF']//text()"))

                        logger.debug(f"sub_sense_num: {sub_sense_num}")
                        logger.debug(f"active: {active}")
                        logger.debug(f"geo: {geo}")
                        logger.debug(f"main_definition: {main_definition}")
                        logger.debug(f"syn: {syn}")

                        for example in sub_sense.xpath("span[@class='EXAMPLE']"):
                            example_text = self._filter_definition(example.xpath("text()"))
                            example_audio = example.xpath("span[1]//@data-src-mp3")

                            logger.debug(f"example_text: {example_text}")
                            logger.debug(f"example_audio: {example_audio}")

                        for collocation_example in sub_sense.xpath("span[@class='ColloExa']"):
                            collocation_text = self._filter_definition(collocation_example.xpath("span[1]//text()"))
                            collocation_audio = collocation_example.xpath("span[2]//@data-src-mp3")

                            logger.debug(f"collocation_text: {collocation_text}")
                            logger.debug(f"collocation_audio: {collocation_audio}")

        logger.debug("######################################################")
        return dict(definitions)
