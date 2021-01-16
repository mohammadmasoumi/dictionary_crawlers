import logging

logger = logging.getLogger(__name__)

LONGMAN_SITE_URL = "https://www.ldoceonline.com"


class LongManDefinitionService:
    _HEADER_XPATH_MAPPING = {
        'hwd': "//span[@class='HWD']//text()",
        'hyphenation': "//span[@class='HYPHENATION']//text()",
        'homnum': "//span[@class='HOMNUM']//text()",
        'pos': "//span[@class='POS']//text()",
        'british_pron': "//span[contains(@class, 'brefile')]/@data-src-mp3",
        'american_pron': "//span[contains(@class, 'amefile')]/@data-src-mp3",
    }

    def __init__(self, items):
        self._items = items

    @staticmethod
    def _join(iterables: list, strip=True):
        """

        :param iterables: list
        :return:
        """
        word = ''.join(filter(lambda x: not x.startswith('\\'), iterables))
        return word.strip() if strip else word

    @staticmethod
    def _fullpath(href: list):
        """

        :param href:
        :return:
        """
        return ''.join([LONGMAN_SITE_URL, *href])
