# -*- coding: utf-8 -*-

from lxml import etree

# Parse the input file
infile = etree.parse('3-morpheusz.xml')

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
            word = etree.SubElement(sentence, 'w')
            word.set('id', 'w{}.{}.{}'.format(i, j, k))
            for child in tok:
                if child.tag == 'orth':
                    word.text = child.text
                if child.tag == 'lex' and child.get('disamb') == '1':
                    word.set('lem', child.xpath('base')[0].text)
                    word.set('tree', child.xpath('ctag')[0].text)

    # After a chunk with the 'last' attribute, add a new paragraph and reset the sentence counter
    if chunk.get('last'):
        i += 1
        paragraph = etree.SubElement(text, 'p')
        paragraph.set('id', str(i))
        j = 1
    else:
        j += 1

tree = etree.ElementTree(text)
tree.write('3.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
