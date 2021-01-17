import logging

from lxml import etree

from .base import ProcessMixin

logger = logging.getLogger(__name__)

LONGMAN_SITE_URL = "https://www.ldoceonline.com"

__all__ = ('LongManDefinitionService',)


class HeaderProcessor(ProcessMixin):
    __XPATH_MAPPING__ = {
        'hwd': "//span[@class='HWD']//text()",
        'hyphenation': "//span[@class='HYPHENATION']//text()",
        'homnum': "//span[@class='HOMNUM']//text()",
        'pos': "//span[@class='POS']//text()",
        'british_pron': "//span[contains(@class, 'brefile')]/@data-src-mp3",
        'american_pron': "//span[contains(@class, 'amefile')]/@data-src-mp3",
    }

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """
        header = {}
        for key, xpath in self.__XPATH_MAPPING__.items():
            value = root.xpath(xpath)
            header.update({key: self._first(value)}) if value else None
        return header


class SubHeaderProcessor(ProcessMixin):
    __XPATH_MAPPING__ = {
        'number': "span[1]//text()",
        'active': "span[@class='ACTIV']//text()",
        'geo': "span[@class='GEO']//text()",
        'syn': "span[@class='SYN']/text()",
        'main_def': "span[@class='DEF']//text()",
        'sign_post': "span[@class='SIGNPOST']//text()",
        'gram': "span[@class='GRAM']//text()",
        'field': "span[@class='FIELD']//text()",
    }

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """
        header = {}
        for key, xpath in self.__XPATH_MAPPING__.items():
            value = root.xpath(xpath)
            header.update({key: self._join(value)}) if value else None
        return header


class RefProcessor(ProcessMixin):
    __XPATH__ = "span[@class='Crossref']/a"

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """
        items = []
        for cross_ref in root.xpath(self.__XPATH__):
            items.append({
                'example': self._join(cross_ref.xpath("@title")),
                'link': self._join_url(LONGMAN_SITE_URL, cross_ref.xpath("@href"))
            })
        return items


class ExampleProcessor(ProcessMixin):
    __XPATH__ = "span[@class='EXAMPLE']"

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """

        items = []
        for example in root.xpath():
            items.append({
                'example': self._join(example.xpath("text()")),
                'audio': self._first(example.xpath("span[1]//@data-src-mp3"))
            })
        return items


class GrammarExampleProcessor(ProcessMixin):
    __XPATH__ = "span[@class='GramExa']"

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """
        items = []
        for grammar_example in root.xpath(self.__XPATH__):
            items.append({
                'example': self._join(grammar_example.xpath("span[1]//text()")),
                'audio': self._first(grammar_example.xpath("span[2]//@data-src-mp3")),
                'text': self._join(grammar_example.xpath("span[2]/text()"))
            })
        return items


class CollocationExampleProcessor(ProcessMixin):
    __XPATH__ = "span[@class='ColloExa']"

    def __call__(self, root, *args, **kwargs):
        """

        :param root:
        :param args:
        :param kwargs:
        :return:
        """
        items = []
        for collocation_example in root.xpath(self.__XPATH__):
            items.append({
                'example': self._join(collocation_example.xpath("span[1]//text()")),
                'audio': self._first(collocation_example.xpath("span[2]//@data-src-mp3"))
            })
        return items


class IdocProcessor:
    __EXAMPLE_ITEMS__ = {
        "header": SubHeaderProcessor(),
        "refs": RefProcessor(),
        "examples": ExampleProcessor(),
        "grammar_examples": GrammarExampleProcessor(),
        "collocation_examples": CollocationExampleProcessor()
    }

    def __init__(self, root):
        """

        :param root:
        """
        self.root = root

    @staticmethod
    def __extract_header__(root):
        return HeaderProcessor()(root)

    @staticmethod
    def __extract_sense(root):
        definition = {}
        for key, processor in IdocProcessor.__EXAMPLE_ITEMS__.items():
            processed_items = processor(root)
            definition.update({key: processed_items}) if processed_items else None
        return definition

    def process(self):
        """

        :return:
        """
        definitions = []

        for html in self.root.xpath("//span[@class='ldoceEntry Entry']"):
            headers = self.__extract_header__(html)

            if headers:
                senses = []
                for sense in html.xpath("//span[@class='Sense']"):
                    sense_item = self.__extract_sense(sense)

                    sub_senses = []
                    for sub_sense in sense.xpath("span[@class='Subsense']"):
                        sub_senses.append(self.__extract_sense(sub_sense))

                    sense_item.update({'sub_senses': sub_senses}) if sub_senses else None
                    senses.append(sense_item)

                headers['senses'] = senses
                definitions.append(headers)

        return definitions


class CorpusProcessor(ProcessMixin):

    def __init__(self, root):
        self.root = root

    def process(self):
        corpus = {}

        for html in self.root.xpath(f"//span[contains(@class, 'exaGroup')]"):
            title = self._first(html.xpath("//span[@class='title']//text()"))
            examples = []
            for elem in html.xpath(f"//span[contains(@class, 'cexa1g')]"):
                example = self._join(elem.xpath("string()"))
                # remove the first dot
                examples.append(example[1:].strip())

            corpus[title] = examples


class LongManDefinitionService(ProcessMixin):

    def process(self, iterable):
        """

        :param iterable:
        :return:
        """
        definitions = {}

        for idx, element in enumerate(iterable):
            iterable_item = element.strip() if isinstance(element, str) else None

            if iterable_item:
                root = etree.HTML(iterable_item)
                idocs = IdocProcessor(root).process()

        return definitions
