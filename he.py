# -*- coding: utf-8 -*-

import argparse

from lxml import etree


def process(file_in, file_out):
    in_tree = etree.parse(file_in)

    text = etree.Element('text')

    for p in in_tree.xpath('//paragraph'):
        paragraph = etree.SubElement(text, 'p')
        paragraph.set('id', p.get('id'))

        for s in p:
            sentence = etree.SubElement(paragraph, 's')
            sentence.set('id', 's{}.{}'.format(p.get('id'), s.get('id')))

            i = 1
            for token in s:
                best = None
                for analysis in token:
                    if best is None or float(analysis.get('score')) > float(best.get('score')):
                        best = analysis

                has_prefix = False
                for c in best:
                    word = etree.SubElement(sentence, 'w')
                    word.set('id', 'w{}.{}.{}'.format(p.get('id'), s.get('id'), i))

                    if c.tag == 'prefix':
                        word.text = c.get('surface')
                        word.set('tree', c.get('function'))
                        has_prefix = True
                        prefix = word.text

                    elif c.tag == 'suffix':
                        prev = word.getprevious()
                        prev.text = token.get('surface')
                        sentence.remove(word)
                        i -= 1

                    elif c.tag == 'base':
                        word.text = token.get('surface')[len(prefix):] if has_prefix else token.get('surface')
                        word.set('lem', c.get('lexiconItem', token.get('surface')))
                        if len(c):
                            if c[0].tag == 'verb':
                                word.set('tree', 'verb-{}{}{}'.format(c[0].get('number', '-')[0], c[0].get('person', '-'), c[0].get('tense', '')))
                            else:
                                word.set('tree', c[0].tag)

                    i += 1

    tree = etree.ElementTree(text)
    tree.write(file_out, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
