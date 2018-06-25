#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json


if __name__ == '__main__':
    _, module_name = sys.argv

    module = __import__(module_name, locals(), globals())
    module.run()
