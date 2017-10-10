# -*- coding: utf-8 -*-

import argparse


def process(file_in, file_out):
    with open(file_in, 'r') as f:
        lines = []
        new_line = ''
        for line in f:
            line = line.strip()
            if line == '':
                lines.append(new_line.strip())
                lines.append('\n\n')
                new_line = ''
            else:
                new_line += line + ' '

        with open(file_out, 'w') as g:
            g.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str, help='Input file')
    parser.add_argument('file_out', type=str, help='Output file')
    args = parser.parse_args()

    process(args.file_in, args.file_out)
