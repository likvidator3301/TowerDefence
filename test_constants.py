#!/usr/bin/env python3

import pytest
import sys
from CrotysEngine import Constants


class TestConstants:

    def test_delimiter(self):
        if sys.platform == 'win32':
            Constants.DELIMITER == '\\'
        elif sys.platform == 'linux':
            Constants.DELIMITER == '/'
