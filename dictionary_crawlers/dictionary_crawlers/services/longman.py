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

    def _process_sub_sense(self, tree):
        """

        :param tree:
        :return:
        """
        return {
            'sub_sense_num': self._join(tree.xpath("span[1]//text()")),
            'active': self._join(tree.xpath("span[@class='ACTIV']//text()")),
            'geo': self._join(tree.xpath("span[@class='GEO']//text()")),
            'syn': self._join(tree.xpath("span[@class='SYN']//text()")),
            'main_definition': self._join(tree.xpath("span[@class='DEF']//text()")),
        }

    def process(self):
        definitions = {}

        logger.debug("######################################################")
        for item in self._items:
            iterable_item = item.strip() if isinstance(item, str) else None

            if iterable_item:
                html = etree.HTML(iterable_item)

                headers = self._process_header(html)
                refs = self._process_refs(tree=html)
                examples = self._process_example(tree=html)
                collocation_examples = self._process_collocation_example(tree=html)
                grammar_examples = self._process_grammar_example(tree=html)

                logger.debug(f"headers: {headers}")
                logger.debug(f"refs: {refs}")
                logger.debug(f"examples: {examples}")
                logger.debug(f"collocation_examples: {collocation_examples}")
                logger.debug(f"grammar_examples: {grammar_examples}")

                # definition
                for sense in html.xpath("//span[@class='Sense']"):
                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    process_sense = self._process_sense(tree=sense)

                    logger.debug(f"process_sense: {process_sense}")

                    for sub_sense in sense.xpath("span[@class='Subsense']"):
                        process_sub_sense = self._process_sub_sense(tree=sub_sense)
                        sub_refs = self._process_refs(tree=html)
                        sub_examples = self._process_example(tree=html)
                        sub_collocation_examples = self._process_collocation_example(tree=html)
                        sub_grammar_examples = self._process_grammar_example(tree=html)

                        logger.debug(f"process_sub_senseL {process_sub_sense}")
                        logger.debug(f"sub_refsL {sub_refs}")
                        logger.debug(f"sub_examplesL {sub_examples}")
                        logger.debug(f"sub_collocation_examplesL {sub_collocation_examples}")
                        logger.debug(f"sub_grammar_examplesL {sub_grammar_examples}")

                    logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        return definitions
