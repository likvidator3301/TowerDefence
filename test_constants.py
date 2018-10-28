#!/usr/bin/env python3

import sys
from CrotysEngine import Constants


class TestConstants:

    def test_delimiter(self):
        if sys.platform == 'win32':
            assert Constants.DELIMITER == '\\'
        elif sys.platform == 'linux':
            assert Constants.DELIMITER == '/'
