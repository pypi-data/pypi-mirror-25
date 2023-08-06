# -*- coding: utf-8 -*-
u"""Front-end command line for :mod:`bnlcrl`.

See :mod:`pykern.pkcli` for how this module is used.

:copyright: Copyright (c) 2016 mrakitin.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import sys

from pykern import pkcli


def main():
    return pkcli.main('bnlcrl')


if __name__ == '__main__':
    sys.exit(main())
