import logging

from lxml import etree

from .base import BaseService

logger = logging.getLogger(__name__)

LONGMAN_SITE_URL = "https://www.ldoceonline.com"


class LongManDefinitionService(BaseService):
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

    def _process_header(self, tree):
        """

        :param tree:
        :return:
        """

        header = {}
        for key, xpath in self._HEADER_XPATH_MAPPING.items():
            value = tree.xpath(xpath)
            header.update({key: value[-1]}) if value else None

        return header

    def _process_example(self, tree):
        """

        :param tree:
        :return:
        """
        items = []
        for example in tree.xpath("span[@class='EXAMPLE']"):
            items.append({
                'example': self._join(example.xpath("text()")),
                'audio': example.xpath("span[1]//@data-src-mp3")
            })
        return items

    def _process_grammar_example(self, tree):
        """

        :param tree:
        :return:
        """
        items = []
        for grammar_example in tree.xpath("span[@class='GramExa']"):
            items.append({
                'example': self._join(grammar_example.xpath("span[1]//text()")),
                'audio': grammar_example.xpath("span[2]//@data-src-mp3")
            })
        return items

    def _process_collocation_example(self, tree):
        """

        :param tree:
        :return:
        """
        items = []
        for collocation_example in tree.xpath("span[@class='ColloExa']"):
            items.append({
                'example': self._join(collocation_example.xpath("span[1]//text()")),
                'audio': collocation_example.xpath("span[2]//@data-src-mp3")
            })
        return items

    def _process_refs(self, tree):
        """

        :param tree:
        :return:
        """
        items = []
        for cross_ref in tree.xpath("span[@class='Crossref']//a"):
            items.append({
                'example': self._join(cross_ref.xpath("@title")),
                'audio': self._join_url(LONGMAN_SITE_URL, cross_ref.xpath("@href"))
            })
        return items

    def _process_sense(self, tree):
        """

        :param tree:
        :return:
        """
        return {
            'sense_num': self._join(tree.xpath("span[1]//text()")),
            'sign_post': self._join(tree.xpath("span[@class='SIGNPOST']//text()")),
            'gram': self._join(tree.xpath("span[@class='GRAM']//text()")),
        }

    def process(self):
        definitions = {}

        logger.debug("######################################################")
        for item in self._items:
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                html = etree.HTML(iterable_item)

                headers = self._process_header(html)

                # definition
                for sense in html.xpath("//span[@class='Sense']"):
                    # logger.debug(etree.tostring(sense))
                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")


                    # cross refs

                    for sub_sense in sense.xpath("span[@class='Subsense']"):
                        sub_sense_num = self._join(sub_sense.xpath("span[1]//text()"))
                        active = self._join(sub_sense.xpath("span[@class='ACTIV']//text()"))
                        geo = self._join(sub_sense.xpath("span[@class='GEO']//text()"))
                        syn = self._join(sub_sense.xpath("span[@class='SYN']//text()"))
                        main_definition = self._join(sub_sense.xpath("span[@class='DEF']//text()"))

                    logger.debug(f"sub_sense_num: {sub_sense_num}")
                    logger.debug(f"active: {active}")
                    logger.debug(f"geo: {geo}")
                    logger.debug(f"main_definition: {main_definition}")
                    logger.debug(f"syn: {syn}")

                    for example in sub_sense.xpath("span[@class='EXAMPLE']"):
                        example_text = self._join(example.xpath("text()"))
                    example_audio = example.xpath("span[1]//@data-src-mp3")

                    logger.debug(f"example_text: {example_text}")
                    logger.debug(f"example_audio: {example_audio}")

                    for collocation_example in sub_sense.xpath("span[@class='ColloExa']"):
                        collocation_text = self._join(collocation_example.xpath("span[1]//text()"))
                    collocation_audio = collocation_example.xpath("span[2]//@data-src-mp3")

                    logger.debug(f"collocation_text: {collocation_text}")
                    logger.debug(f"collocation_audio: {collocation_audio}")

                    logger.debug("######################################################")
