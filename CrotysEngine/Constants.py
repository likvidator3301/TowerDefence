#!/usr/bin/env python3

import sys
import os

DELIMITER = ''

if sys.platform == 'win32':
    DELIMITER = '\\'
elif sys.platform == 'linux':
    DELIMITER = '/'
else:
    sys.exit()
