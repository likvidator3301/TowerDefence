#!/usr/bin/env python3

import sys

DELIMITER = ''
if sys.platform == 'win32':
    DELIMITER = '\\'
elif sys.platform == 'linux':
    DELIMITER = '/'
else:
    sys.exit()
