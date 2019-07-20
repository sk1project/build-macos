# -*- coding: utf-8 -*-
#
#   Build config for UniConvertor 2.x on macOS
#
# 	Copyright (C) 2019 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys

UC2DIR = "/opt/uniconvertor"
PY_DIR = '%s/lib/python2.7/site-packages' % UC2DIR
PKG_DIR = '%s/pkgs' % UC2DIR
CUR_DIR = os.getcwd()

MAIN_BUILD = '--test' not in sys.argv and '-t' not in sys.argv
VERBOSE = '-v' in sys.argv or '--verbose' in sys.argv


PREFIX = "--prefix=%s" % UC2DIR
TRACK = "--disable-dependency-tracking"

LOG = ' >>%s/build.log 2>>%s/build.log' % (CUR_DIR, CUR_DIR) \
    if not VERBOSE else ''
