# -*- coding: utf-8 -*-

import argparse
import codecs

from lxml import etree


def process(file_in, file_out):
    with codecs.open(file_in, 'r', encoding='utf-8') as f:
        text = etree.Element('text')

        i = j = k = 0
        paragraph_start = sentence_start = True

        for line in f:
            line = line.strip()

            if not line:
                paragraph_start = True
                continue

            if paragraph_start:
                i += 1
                j = 0
                paragraph = etree.SubElement(text, 'p')
                paragraph.set('id', str(i))
                paragraph_start = False
                sentence_start = True

            if sentence_start:
                j += 1
                k = 0
                sentence = etree.SubElement(paragraph, 's')
                sentence.set('id', 's{}.{}'.format(i, j))
                sentence_start = False

            w, tag, lemma = line.split('\t')

            k += 1
            word = etree.SubElement(sentence, 'w')
            word.set('id', 'w{}.{}.{}'.format(i, j, k))
            word.text = w
            word.set('tree', tag)
            word.set('lem', lemma)

            # The 'SENT' marks a sentence end
            if tag == 'SENT':
                sentence_start = True

        tree = etree.ElementTree(text)
        tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
