# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4: sw=4: et

"""
@see: https://docs.scrapy.org/en/latest/topics/media-pipeline.html#topics-media-pipeline-enabling
"""
import logging

from scrapy.pipelines.files import FilesPipeline

logger = logging.getLogger(__name__)


class DictionaryFilePipeline(FilesPipeline):

    def file_downloaded(self, response, request, info, *, item=None):
        logger.debug("File Downloaded ............")
        super(DictionaryFilePipeline, self).file_downloaded(response, request, info, item=None)

    def item_completed(self, results, item, info):
        logger.info("File Completed ................")
        super(DictionaryFilePipeline, self).item_completed(results, item, info)
