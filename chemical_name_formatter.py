#!/usr/bin/env python3
''' create properly formatted unicode chemical names '''

trans = str.maketrans('0123456789.-','₀₁₂₃₄₅₆₇₈₉₋')

def main(string):
   print(make_subscripts(string))


def make_subscripts(string):
   return string.translate(trans)


if __name__ == '__main__':
   import plac; plac.call(main)