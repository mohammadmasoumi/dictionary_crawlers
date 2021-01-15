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


# CUSTOMIZED_MATCH_PATTERN = r"\{\{(?:\s)*([^|}]+)(?:\s)*\|(?:\s)*([^|}]+)(?:\s)*\}\}"
# CUSTOMIZED_SUB_PATTERN = "\{{\{{(?:\s)*{tag_key}(?:\s)*\|(?:\s)*([^|}}]+)(?:\s)*\}}\}}"  # NOQA

class HeaderProcessor:
    _KEY_PATTERN_MAPPING = {
        'hwd': '<span class=\"HWD\">(?:\s)*([^<}]+)</span>',
        'hyphenation': '<span class=\"HYPHENATION\">(?:\s)*([^<}]+)</span>',
        'homnum': '<span class=\"HOMNUM\">(?:\s)*([^<}]+)</span>',
        'pos': '<span class=\"POS\">(?:\s)*([^<}]+)</span>',
    }

    def __call__(self, iterable, **kwargs):
        """
        :param iterable: xpath query result
        :param kwargs: scrapy context
        :return:
        """

        headers = defaultdict(dict)

        logger.debug("######################################################")
        for item in iterable:
            # logger.info(item)
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                for key, pattern in self._KEY_PATTERN_MAPPING.items():
                    re_object = re.compile(pattern, re.IGNORECASE)
                    values = re.findall(re_object, iterable_item)
                    logger.info(f"MATCH --> {key}: {values}")

        logger.debug("######################################################")

        return dict(headers)
