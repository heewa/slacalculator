#!/usr/bin/env python
"""For quick testing on cmdline, you can run this file with arguments to be
parsed as text for formulas, like:
    python cmdline.py 'What is 1 + 2?'
"""
from sys import argv

from calc import find_and_calc


if __name__ == '__main__':
    for arg in argv[1:]:
        print '==] %s' % arg
        for index, (formula, result) in enumerate(find_and_calc(arg) or []):
            print '  #%d  %s  --> %s' % (index + 1, formula, result)
