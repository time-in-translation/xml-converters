# -*- coding: utf-8 -*-

import argparse
import codecs

from lxml import etree


def process(file_in, file_out):
    with codecs.open(file_in, 'r', 'utf-8') as f:
        text = etree.Element('text')

        i = 1
        for line in f:
            line = line.strip()

            if not line:
                i += 1
                continue

            paragraph = etree.SubElement(text, 'p')
            paragraph.set('id', str(i))

            j = 1
            sentence = etree.SubElement(paragraph, 's')
            sentence.set('id', 's{}.{}'.format(i, j))

            k = 1
            for wt in line.split('$'):
                if not wt:
                    continue

                if len(wt.split('/', 1)) >= 2:  # If there is an analysis...
                    word, lt = wt.split('/', 1)  # Split word from analysis

                    lt0 = lt.split('/')[0]  # Take the first analysis
                    before, w = word.split('^')

                    if before.strip():
                        b = before.strip()

                        word = etree.SubElement(sentence, 'w')
                        word.set('id', 'w{}.{}.{}'.format(i, j, k))
                        word.text = b
                        word.set('lem', b)
                        word.set('tree', '')
                        k += 1

                    if lt0.startswith('*'):  # A star denotes no analysis is
                        w = w.strip()
                        lemma = w
                        tree = ''

                    else:
                        l, t = lt0.split('<', 1)  # Split lemma from part of speech

                        w = w.strip()
                        lemma = l.strip()
                        tree = t.replace('><', '-').replace('<', '-').replace('>', '')  # Replace <> with dashes
                else:
                    w = wt.strip()
                    lemma = wt.strip()
                    tree = ''

                word = etree.SubElement(sentence, 'w')
                word.set('id', 'w{}.{}.{}'.format(i, j, k))
                word.text = w
                word.set('lem', lemma)
                word.set('tree', tree)
                k += 1

                # sent marks a sentence end, create a new sentence SubElement and reset the word counter (k)
                if tree == 'sent':
                    j += 1
                    sentence = etree.SubElement(paragraph, 's')
                    sentence.set('id', 's{}.{}'.format(i, j))
                    k = 1

        tree = etree.ElementTree(text)
        tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
