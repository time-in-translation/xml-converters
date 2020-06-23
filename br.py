# -*- coding: utf-8 -*-

import argparse
import codecs
import re

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

            line = line.replace('^./.<sent>$^./.<sent>$^./.<sent>$', '^.../...<ellipsis>$')  # fixes ellipsis
            line = line.replace('$^!/!<sent>$”', '$^!/!<punct>$”')  # !” is not a sentence ending
            line = line.replace('$^?/?<sent>$”', '$^?/?<punct>$”')  # ?” is not a sentence ending

            paragraph = etree.SubElement(text, 'p')
            paragraph.set('id', str(i))

            j = 1
            sentence = etree.SubElement(paragraph, 's')
            sentence.set('id', 's{}.{}'.format(i, j))

            results = []
            wts = re.split(r'\^(.*?)\$', line)
            for n, wt in enumerate(wts):
                if n % 2 == 0:
                    w = wt.strip()
                    if w:
                        ws = w.split()
                        for w in ws:
                            results.append([w, w, 'punct'])
                    continue

                elif len(wt.split('/', 1)) >= 2:  # If there is an analysis...
                    w, lt = wt.split('/', 1)  # Split word from analysis

                    lt0 = lt.split('/')[0]  # Take the first analysis

                    if lt0.startswith('*'):  # A star denotes no analysis was found
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

                results.append([w, lemma, tree])

            k = 1
            for n, wlt in enumerate(results):
                # Add dialogue markers in the first position to the previous sentence
                if wlt[0] in [u'”', u'»'] and k == 1:
                    word = etree.SubElement(prev_s, 'w')
                    word.set('id', 'w{}.{}.{}'.format(i, prev_j, prev_k))
                    k = 0
                    prev_k += 1
                    # Remove the current sentence if this was the last word of the paragraph.
                    if n == len(results) - 1:
                        paragraph.remove(sentence)
                else:
                    word = etree.SubElement(sentence, 'w')
                    word.set('id', 'w{}.{}.{}'.format(i, j, k))

                word.text = wlt[0]
                word.set('lem', wlt[1])
                word.set('tree', wlt[2])
                k += 1

                # sent marks a sentence end, create a new sentence SubElement and reset the word counter (k)
                if wlt[2] == 'sent' and n != len(results) - 1:
                    prev_j = j
                    prev_k = k
                    prev_s = sentence

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
