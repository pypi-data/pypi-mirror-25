#!/usr/bin python3.6

import os
import argparse

__author__ = 'Oleksandr Rypiuk'


def get_sorted_file_size(the_path, number, min_first):

    # get result
    result = {}
    for root, dirs, files in os.walk(the_path):
        for fn in files:
            path = os.path.join(root, fn)
            try:
                size = os.stat(path).st_size
            except FileNotFoundError:
                print('No such file or directory:', path)
                return
            result[path] = size
    result = sorted(result.items(), key=lambda x: x[1], reverse=not min_first)

    # set table size
    size_len = len(str(result[0][1])) if not min_first else len(str(result[number-1][1]))
    number_len = len(str(number))
    mb_len = size_len - 6 if size_len - 6 > 0 else 1

    # additional information
    print(f'Path: {the_path}')
    print(f'Number of files: {len(result)}')

    # header
    print(f'{"№":>{number_len}} | {"B":^{size_len}} | {"MB":^{mb_len+2}} | Path')

    # check if number args > number of files
    if number > len(result):
        number = len(result)

    # content
    for i in range(number):
        print(f'{i+1:{number_len}} | {result[i][1]:{size_len}} | '
              f'{result[i][1] * 0.000001:{mb_len+2}.1f} | {result[i][0]}')


def main():
    parser = argparse.ArgumentParser(description='Displays sorted information about size, '
                                                 'path to files in subdirectories.')
    parser.add_argument('-p', dest='path', metavar='PATH', help='the path to parent dir', action='store',
                        default=os.getcwd())
    parser.add_argument('-n', type=int, dest='number', metavar='NUMBER', help='how much files will be shown',
                        action='store', default=5)
    parser.add_argument('-m', '--min', help='sort by min size', action='store_true')

    args = parser.parse_args()
    get_sorted_file_size(the_path=args.path, number=args.number, min_first=args.min)

if __name__ == '__main__':
    main()
