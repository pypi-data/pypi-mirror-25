#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys

from validators import filter_using_re


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    try:
        content = read_file(sys.argv[1])
        evaluation = evaluate_characters(content)

        print(get_evaluated_string(evaluation))

    except IndexError:
        print("It's mandatory to supply a path")


def get_evaluated_string(evaluation):
    evaluated_string = ''

    for e in evaluation:
        if e['flagged'] == 'NULL':
            evaluated_string += Colors.WARNING + '[NULL]' + Colors.ENDC
        elif e['flagged'] == '4-BYTE':
            evaluated_string += Colors.OKGREEN + '[' + e['character'] + ']' + Colors.ENDC
        elif e['flagged'] == 'UTF-8':
            evaluated_string += Colors.OKBLUE + '[' + e['character'] + ']' + Colors.ENDC
        else:
            evaluated_string += e['character']

    return evaluated_string


def read_file(path):
    try:
        with io.open(path, mode='r', encoding='utf-8') as fp:
            return fp.read()
    except UnicodeDecodeError:
        try:
            with open(path, mode='r') as fp:
                return fp.read()
        except UnicodeDecodeError:
            print(path + ' seems to be a non UTF-8 file')
            exit()


def evaluate_characters(content):
    evaluation = []

    for i in content:
        character = {
            'character': i,
            'flagged': False
        }

        try:
            d = i

            if d == '\x00':
                character['flagged'] = 'NULL'
            elif filter_using_re(d) != d:
                character['flagged'] = '4-BYTE'
        except UnicodeError:
            character['flagged'] = 'UTF-8'

        evaluation.append(character)
    return evaluation

if __name__ == "__main__":
    main()
