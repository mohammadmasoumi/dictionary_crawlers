#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

from logging import getLogger

from itemloaders.processors import TakeFirst

logger = getLogger(__name__)

__all__ = (
    "default_input_processor",
    "default_output_processor"
)

default_input_processor = TakeFirst()
default_output_processor = TakeFirst()
