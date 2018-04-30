# -*- coding: utf-8 -*-

import argparse
import codecs

from lxml import etree


def process(file_in, file_out, sentence_tokenized=False):
    with codecs.open(file_in, 'r', encoding='utf-8') as f:
        text = etree.Element('text')

        i = j = k = 0
        paragraph_start = sentence_start = True

        for n, line in enumerate(f):
            line = line.strip()

            if not line:
                if sentence_tokenized and not sentence_start:
                    sentence_start = True
                else:
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

            # Split into word, tag and lemma (or word and tag if this line only contains two values)
            split_line = line.split('\t')
            if 1 <= len(split_line) <= 3:
                w = split_line[0]
                tag = ''
                lemma = ''

                if len(split_line) >= 2:
                    tag = split_line[1]

                    if len(split_line) >= 3:
                        lemma = split_line[2]
            else:
                raise ValueError('Incorrect number at line {}'.format(n))

            k += 1
            word = etree.SubElement(sentence, 'w')
            word.set('id', 'w{}.{}.{}'.format(i, j, k))
            word.text = w
            if tag:
                word.set('tree', tag)
            if lemma:
                word.set('lem', lemma)

            # The 'SENT' marks a sentence end in Greek, Z.Fst, Z.Int, Z.Exc for Estonian
            if not sentence_tokenized and tag in ['SENT', 'Z.Fst', 'Z.Int', 'Z.Exc']:
                sentence_start = True

        tree = etree.ElementTree(text)
        tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    parser.add_argument('--tok', action='store_true', help='Is the file sentence-tokenized?')
    args = parser.parse_args()

    process(args.file_in, args.file_out, args.tok)
