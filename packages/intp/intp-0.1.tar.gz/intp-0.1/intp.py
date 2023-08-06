import sys
from ConfigParser import ConfigParser
from collections import namedtuple


def main():
    args = sys.argv
    if len(args) < 4:
        print("usage: {} <ini with vars> <ini-that-needs-interpolation> <interpolated-ini>".format(args[0]))
        exit(1)
    vars_ini_fn, src_ini_fn, target_ini_fn = sys.argv[1:]
    src_ini = ConfigParser()
    src_ini.read(vars_ini_fn)

    sections = {}
    for section in src_ini.sections():
        items = dict(src_ini.items(section))
        tpt = namedtuple(section, items.keys())
        sections[section] = tpt._make(items.values())

    with open(src_ini_fn) as sf:
        src_ini = sf.read()

    with open(target_ini_fn, 'w') as tf:
        try:
            tf.write(src_ini.format(**sections))
        except AttributeError as e:
            print('Interpolation error: {}'.format(e.message))


if __name__ == '__main__':
    main()
