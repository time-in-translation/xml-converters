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

            tokens = line.split()
            end_after_next = False
            k = 0
            for n, wt in enumerate(tokens):
                w, t = wt.split('#')

                word = etree.SubElement(sentence, 'w')
                k += 1
                word.set('id', 'w{}.{}.{}'.format(i, j, k))
                word.text = w
                word.set('tree', t)

                # The '。' marks a sentence end, create a new sentence SubElement,
                # unless the next character is an end quote, or
                # unless this is the last character of the line
                if w == '。' or end_after_next:
                    if n + 1 == len(tokens):
                        continue
                    else:
                        next_w, next_t = tokens[n + 1].split('#')
                        if next_w == '”':
                            end_after_next = True
                            continue

                        j += 1
                        sentence = etree.SubElement(paragraph, 's')
                        sentence.set('id', 's{}.{}'.format(i, j))
                        k = 0
                        end_after_next = False

        tree = etree.ElementTree(text)
        tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
