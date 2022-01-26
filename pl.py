# -*- coding: utf-8 -*-

import argparse

from lxml import etree


def process(in_file, out_file):
    # Parse the input file
    infile = etree.parse(in_file)

    # Create counters for paragraphs and sentences
    i = j = 1

    # Start a text element and add a first paragraph
    text = etree.Element('text')
    paragraph = etree.SubElement(text, 'p')
    paragraph.set('id', str(i))

    # Loop over the chunks, add sentences
    for chunk in infile.getroot():
        for s in chunk:
            sentence = etree.SubElement(paragraph, 's')
            sentence.set('id', 's{}.{}'.format(i, j))
            for k, tok in enumerate(s.xpath('tok'), start=1):
                # If we find a $ token, add a new paragraph and reset the sentence counter
                if tok.getchildren()[0].text == '$':
                    if len(sentence) == 0:
                        sentence.getparent().remove(sentence)

                    i += 1
                    paragraph = etree.SubElement(text, 'p')
                    paragraph.set('id', str(i))
                    j = 1
                    sentence = etree.SubElement(paragraph, 's')
                    sentence.set('id', 's{}.{}'.format(i, j))
                    continue

                word = etree.SubElement(sentence, 'w')
                word.set('id', 'w{}.{}.{}'.format(i, j, k))
                for child in tok:
                    if child.tag == 'orth':
                        word.text = child.text
                    if child.tag == 'lex' and child.get('disamb') == '1':
                        word.set('lem', child.xpath('base')[0].text)
                        word.set('tree', child.xpath('ctag')[0].text)

        j += 1

    tree = etree.ElementTree(text)
    tree.write(out_file, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
