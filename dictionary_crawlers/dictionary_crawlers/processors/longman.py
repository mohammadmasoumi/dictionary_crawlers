#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et
# flake8: noqa

import logging
import re
from collections import defaultdict

from ..services import LongManDefinitionService

logger = logging.getLogger(__name__)

__all__ = (
    'LongManFamilyWordProcessor',
    'LongManDefinitionProcessor'
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


class LongManDefinitionProcessor:

    def __call__(self, iterable, *args, **kwargs):
        """

        :param iterable:
        :param args:
        :param kwargs:
        :return:
        """

        return LongManDefinitionService(items=iterable).process()