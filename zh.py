# -*- coding: utf-8 -*-

import argparse

from lxml import etree


def process(file_in, file_out):
    with open(file_in, 'r') as f:
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

            for k, wt in enumerate(line.split(), start=1):
                w, t = wt.split('#')

                word = etree.SubElement(sentence, 'w')
                word.set('id', 'w{}.{}.{}'.format(i, j, k))
                word.text = w
                word.set('tree', t)

                # The '。' marks a sentence end, create a new sentence SubElement,
                # unless this is the last character of the line
                if w == '。' and k != len(line.split()):
                    j += 1
                    sentence = etree.SubElement(paragraph, 's')
                    sentence.set('id', 's{}.{}'.format(i, j))

        tree = etree.ElementTree(text)
        tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
