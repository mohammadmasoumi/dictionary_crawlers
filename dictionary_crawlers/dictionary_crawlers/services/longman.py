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


class LongManDefinitionService(ProcessMixin):

    @staticmethod
    def __extract_header__(root):
        return HeaderProcessor()(root)

    @staticmethod
    def

    def __extract_definition__(self, root):
        """

        :param root:
        :return:
        """
        definition = {}

        refs = self._process_refs(tree=root)
        examples = self._process_example(tree=root)
        collocation_examples = self._process_collocation_example(tree=root)
        grammar_examples = self._process_grammar_example(tree=root)

        definition.update({'refs': refs}) if refs else None
        definition.update({'examples': examples}) if examples else None
        definition.update({'collocation_examples': collocation_examples}) if collocation_examples else None
        definition.update({'grammar_examples': grammar_examples}) if grammar_examples else None

        return

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

                for html in root.xpath("//span[@class='ldoceEntry Entry']"):
                    headers = self.__extract_header__(html)

                    if headers:

                        # definition
                        senses = []
                        for sense in html.xpath("//span[@class='Sense']"):
                            process_sense = self._process_sense(tree=sense)

                            sense_refs = self._process_refs(tree=sense)
                            sense_examples = self._process_example(tree=sense)
                            sense_collocation_examples = self._process_collocation_example(tree=sense)
                            sense_grammar_examples = self._process_grammar_example(tree=sense)

                            process_sense.update({'sense_refs': sense_refs}) if sense_refs else None
                            process_sense.update({'sense_examples': sense_examples}) if sense_examples else None
                            process_sense.update({'sense_collocation_examples': sense_collocation_examples}) \
                                if sense_collocation_examples else None
                            process_sense.update({'sense_grammar_examples': sense_grammar_examples}) if \
                                sense_grammar_examples else None

                            process_sense.update({'sub_senses': []})

                            for sub_sense in sense.xpath("span[@class='Subsense']"):
                                process_sub_sense = self._process_sub_sense(tree=sub_sense)

                                sub_refs = self._process_refs(tree=sub_sense)
                                sub_examples = self._process_example(tree=sub_sense)
                                sub_collocation_examples = self._process_collocation_example(tree=sub_sense)
                                sub_grammar_examples = self._process_grammar_example(tree=sub_sense)

                                process_sub_sense.update({'sub_refs': sub_refs}) if sub_refs else None
                                process_sub_sense.update({'sub_examples': sub_examples}) if sub_examples else None
                                process_sub_sense.update({'sub_collocation_examples': sub_collocation_examples}) \
                                    if sub_collocation_examples else None
                                process_sub_sense.update({'sub_grammar_examples': sub_grammar_examples}) \
                                    if sub_grammar_examples else None

                                process_sense['sub_senses'].append(process_sub_sense)

                            senses.append(process_sense)
                        headers['senses'] = senses
                        definitions[headers['homnum']] = headers

                corpus = {}
                for html in root.xpath(f"//span[@class='exaGroup cexa{idx + 1} exaGroup']"):
                    title = self._first(html.xpath("//span[@class='title']//text()"))
                    examples = []
                    for elem in html.xpath(f"//span[@class='cexa1g{idx + 1} exa']"):
                        example = self._join(elem.xpath("string()"))
                        # remove the first dot
                        examples.append(example[1:].strip())

                    corpus[title] = examples

                definitions.update(corpus=corpus)

        return definitions
