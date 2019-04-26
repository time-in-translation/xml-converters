import argparse
import os
import subprocess

from lxml import etree

from conll_utils import POS_TAGS, CONLL_S_FORMAT, CONLL_W_FORMAT

MALT_COMMAND = 'java -jar {0} -c {1} -m parse -i {2} -o {3}'
MALT_LOCATION = '/opt/maltparser-1.9.2'
MALT_PARSER = 'maltparser-1.9.2.jar'
MALT_CONFIG = '{0}-parser'


def process_single(language, in_file, out_file):
    """
    Converts an OPUS-xml file to the CONLL-U format.
    """
    with open(out_file, 'w') as f:
        tree = etree.parse(in_file)
        for sentence in tree.xpath('//s'):
            f.write(CONLL_S_FORMAT.format(sentence.get('id')))

            words = sentence.xpath('./w')
            for word in words:
                word_id = word.get('id').split('.')[-1]
                word_lem = word.get('lem')
                word_pos = word.get(POS_TAGS[language])

                f.write(CONLL_W_FORMAT.format(word_id, word.text, word_lem, word_pos))

            f.write('\n')


def malt_parse(language, in_file, out_file):
    """
    Parses a CONLL-U file using the MaltParser (http://www.maltparser.org/)
    """
    cwd = os.getcwd()
    file_in = os.path.join(cwd, in_file)
    file_out = os.path.join(cwd, out_file)

    cmd = MALT_COMMAND.format(MALT_PARSER, MALT_CONFIG.format(language), file_in, file_out)
    subprocess.call(cmd, shell=True, cwd=MALT_LOCATION, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('language', help='Language')
    parser.add_argument('file_in', help='Input file')
    parser.add_argument('file_out', help='Output file')
    args = parser.parse_args()

    tmp_file = 'conll.tmp'

    process_single(args.language, args.file_in, tmp_file)
    malt_parse(args.language, tmp_file, args.file_out)
