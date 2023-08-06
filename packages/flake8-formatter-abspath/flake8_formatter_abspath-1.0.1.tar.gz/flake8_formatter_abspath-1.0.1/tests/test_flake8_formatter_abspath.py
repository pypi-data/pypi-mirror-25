#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import optparse
import os

from flake8 import style_guide
from flake8.formatting import default

from flake8_formatter_abspath import AbsolutePathFormatter

filename = './some/file.py'
absfilename = os.path.abspath(filename)

try:
    # 3.4.0
    error = style_guide.Violation('A000', filename, 1, 1, 'wrong wrong wrong', 'import os')
except AttributeError:
    # 3.3.0
    error = style_guide.Error('A000', filename, 1, 1, 'wrong wrong wrong', 'import os')


def options(**kwargs):
    """Create an optparse.Values instance."""
    kwargs.setdefault('output_file', None)
    kwargs.setdefault('tee', False)
    return optparse.Values(kwargs)


def verify_formatter(formatter, filename):
    assert formatter.format(error) == '{}:1:1: A000 wrong wrong wrong'.format(filename)


def test_abspath_formatter():
    absformatter = AbsolutePathFormatter(
        options(show_source=False, format='abspath')
    )
    verify_formatter(absformatter, absfilename)


def test_default_formatter():
    formatter = default.Default(
        options(show_source=False, format='default')
    )
    verify_formatter(formatter, filename)
