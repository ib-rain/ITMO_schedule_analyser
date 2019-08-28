#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from sys import argv, exit


def main():
    if len(argv) != 3:
        print('usage: python '+argv[0]+' load.txt result.csv\n')
        exit(1)

    result = []
    with open(argv[1]) as f:
        content = f.readlines()
    for s in content:
        result.extend(eval(s))

    result = filter(lambda x: x[2] > 0, result)

    with open(argv[2], mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"',
                       quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Classroom #', 'Sum of student-hours',
                    'Max of student-hours'])
        for r in sorted(result, key=lambda x: x[1], reverse=True):
            w.writerow(r)

    return 0


if __name__ == '__main__':
    main()
