#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et
# flake8: noqa

import logging
import re
from collections import defaultdict

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
    _KEY_PATTERN_MAPPING = {
        "hwd": "<span class=\"HWD\">(?:\s)*([^<}]+)</span>",
        "hyphenation": "<span class=\"HYPHENATION\">(?:\s)*([^<}]+)</span>",
        "homnum": "<span class=\"HOMNUM\">(?:\s)*([^<}]+)</span>",
        "pos": "<span class=\"POS\">(?:\s)*([^<}]+)</span>",
    }  # NOQA

    def __call__(self, iterable, **kwargs):
        """
        r"\{\{(?:\s)*([^|}]+)(?:\s)*\|(?:\s)*([^|}]+)(?:\s)*\}\}"
        "\{{\{{(?:\s)*{tag_key}(?:\s)*\|(?:\s)*([^|}}]+)(?:\s)*\}}\}}"
        :param iterable: xpath query result
        :param kwargs: scrapy context
        :return:
        """

        headers = defaultdict(dict)

        logger.debug("######################################################")
        for item in iterable:
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                for key, pattern in self._KEY_PATTERN_MAPPING.items():
                    re_object = re.compile(pattern, re.IGNORECASE)
                    values = re.findall(re_object, iterable_item)
                    logger.info(f"MATCH --> {key}: {values}")

        logger.debug("######################################################")

        return dict(headers)
