import logging

from lxml import etree

from .base import BaseService

logger = logging.getLogger(__name__)

LONGMAN_SITE_URL = "https://www.ldoceonline.com"

__all__ = ('LongManDefinitionService',)


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

        super(LongManDefinitionService, self).__init__(items)

    def _process_header(self, tree):
        """

        :param tree:
        :return:
        """

        header = {}
        for key, xpath in self._HEADER_XPATH_MAPPING.items():
            value = tree.xpath(xpath)
            header.update({key: self._first(value)}) if value else None

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
                'audio': self._first(example.xpath("span[1]//@data-src-mp3"))
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
                'audio': self._first(grammar_example.xpath("span[2]//@data-src-mp3")),
                'text': self._join(grammar_example.xpath("span[2]/text()"))
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
                'audio': self._first(collocation_example.xpath("span[2]//@data-src-mp3"))
            })
        return items

    def _process_refs(self, tree):
        """

        :param tree:
        :return:
        """
        items = []
        for cross_ref in tree.xpath("span[@class='Crossref']/a"):
            items.append({
                'example': self._join(cross_ref.xpath("@title")),
                'link': self._join_url(LONGMAN_SITE_URL, cross_ref.xpath("@href"))
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
            'def': self._join(tree.xpath("span[@class='DEF']//text()")),
            'field': self._join(tree.xpath("span[@class='FIELD']//text()")),
            'active': self._join(tree.xpath("span[@class='ACTIV']//text()")),
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
            'syn': self._join(tree.xpath("span[@class='SYN']/text()")),
            'main_definition': self._join(tree.xpath("span[@class='DEF']//text()")),
        }

    def process(self):
        definitions = {}

        for idx, element in enumerate(self._items):
            iterable_item = element.strip() if isinstance(element, str) else None

            if iterable_item:
                root = etree.HTML(iterable_item)

                for html in root.xpath("//span[@class='ldoceEntry Entry']"):
                    headers = self._process_header(html)

                    if headers:
                        refs = self._process_refs(tree=html)
                        examples = self._process_example(tree=html)
                        collocation_examples = self._process_collocation_example(tree=html)
                        grammar_examples = self._process_grammar_example(tree=html)

                        headers.update({'refs': refs}) if refs else None
                        headers.update({'examples': examples}) if examples else None
                        headers.update({'collocation_examples': collocation_examples}) if collocation_examples else None
                        headers.update({'grammar_examples': grammar_examples}) if grammar_examples else None

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
