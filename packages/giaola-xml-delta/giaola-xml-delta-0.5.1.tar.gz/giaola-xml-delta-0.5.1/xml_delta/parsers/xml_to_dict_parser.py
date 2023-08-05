from .base import Parser

import lxml.etree as ET

import logging
logger = logging.getLogger(__name__)

class XMLToDictParser(Parser):

    data = []

    def __init__(self, flush_counter):
        """
        :param unicode file_path:       File path to parse.
        :param unicode tag:             Element we are interested in.
        """
        super(XMLToDictParser, self).__init__(flush_counter)

    def parse(self, source, tag, **kwargs):
        self.context = ET.iterparse(source,
                                    events=("end",),
                                    huge_tree=True,
                                    recover=True)

        iterator = iter(self.context)

        while True:
            try:
                event, root = iterator.next()

                if root.tag == tag:
                    # Get parsed object
                    element_dict = self.__elem2list(root)[tag]

                    print element_dict

                    # cleanup None values from element_dict
                    element_dict = dict((k, v) for k, v in element_dict.iteritems() if v is not None)

                    self.__clear_element(root)

                    self.data.append(element_dict)

                    self._fire_if_needed(self.data)

            except StopIteration:
                break
            except Exception as e:
                logger.exception(e)

        del self.context

        self._fire_if_needed(self.data, True)

    def __clear_element(self, element):
        element.clear()

        while element.getprevious() is not None:
            del element.getparent()[0]

    def __elem2list(self, elem):
        """Convert an ElementTree element to a list"""

        block = {}

        # get the element's children
        children = elem.getchildren()

        if children:
            cur = map(self.__elem2list, children)

            # create meaningful lists
            scalar = False
            try:
                if elem[0].tag != elem[1].tag:  # [{a: 1}, {b: 2}, {c: 3}] => {a: 1, b: 2, c: 3}
                    cur = dict(zip(
                        map(lambda e: e.keys()[0], cur),
                        map(lambda e: e.values()[0], cur)
                    ))
                else:
                    scalar = True
            except Exception as e:  # [{a: 1}, {a: 2}, {a: 3}] => {a: [1, 2, 3]}
                scalar = True

            if scalar:
                if len(cur) > 1:
                    cur = {elem[0].tag: [e.values()[0] for e in cur if e.values()[0] is not None]}
                else:
                    cur = {elem[0].tag: cur[0].values()[0]}

            block[elem.tag] = cur

        else:
            val = None
            if elem.text:
                val = elem.text.strip()
                val = val if len(val) > 0 else None
            elif elem.attrib:
                val = elem.attrib
                val = val if len(val) > 0 else None

            block[elem.tag] = val

        return block
