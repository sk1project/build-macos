#!/usr/bin/python
#
#   Build for UniConvertor 2.x on macOS
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

import fsutils
from utils import *


# ---------------------------------------------
# Libraries
# ---------------------------------------------

@build_decorator
@catcher
def main(*_args):
    if os.path.exists('/opt/uc2'):
        rm('/opt/uc2')
    run('cp -R %s /opt/uc2' % UC2DIR)
    run('rm -rf %s/bin/*' % UC2DIR)
    rm('%s/share' % UC2DIR)
    rm('%s/var' % UC2DIR)
    rm('%s/include' % UC2DIR)
    run('rm -rf %s/lib/*.a' % UC2DIR)
    run('rm -rf %s/lib/*.la' % UC2DIR)
    rm('%s/lib/pkgconfig' % UC2DIR)
    rm('%s/lib/python2.7' % UC2DIR)
    run('rm -rf %s/pkgs/PIL/*.py' % UC2DIR)

    links = fsutils.get_symlinks(UC2DIR)
    links += [('/opt/uniconvertor/bin/uniconvertor',
               '/usr/local/bin/uniconvertor'),
              ('/opt/uniconvertor/bin/uniconvertor',
               '/usr/local/bin/uc2')]
    for _path, link in links:
        if os.path.exists(link):
            os.remove(link)
    with open('%s/symlinks' % UC2DIR, 'wb') as fileptr:
        fileptr.write(repr(links))

    if not os.path.exists('./dist'):
        mkdirs('./dist')
    if os.path.exists('./dist/cache.zip'):
        os.remove('./dist/cache.zip')

    run('zip -ro9X dist/cache.zip %s' % UC2DIR)
    rm(UC2DIR)
    run('mv /opt/uc2 %s' % UC2DIR)


if __name__ == '__main__':
    main('')
    echo('CACHE BUILD SUCCESSFUL!', WHITE, eol=True, to_log=True)
