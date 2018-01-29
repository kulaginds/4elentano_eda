#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from chelentanoeda import ChelentanoEda, ChelentanoEdaException


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Help to run:')
        print('./script.py config.json')
        sys.exit(-1)

    config_file = sys.argv[1]

    try:
        eda = ChelentanoEda(config_file)
        eda.run()
    except ChelentanoEdaException as e:
        print(e)
