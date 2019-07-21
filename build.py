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

from utils import *

# ---------------------------------------------
# Libraries
# ---------------------------------------------
PKGCFG = "pkg-config-0.29.2"
ZLIB = "zlib-1.2.11"
LIBPNG = "libpng-1.6.37"
FREETYPE = "freetype-2.9"
PIXMAN = "pixman-0.38.2"
CAIRO = "cairo-1.16.0"
LCMS = "lcms2-2.9"
GETTEXT = "gettext-0.20.1"
PCRE = "pcre-8.43"
FFI = "libffi-3.2.1"
GLIB = "glib-2.55.2"
FONTCFG = "fontconfig-2.13.91"
FRIBIDI = "fribidi-1.0.5"
DATRIE = "libdatrie-0.2.12"
THAI = "libthai-0.1.28"
GRAPH = "graphite2-1.3.12"
HARFBUZZ = "harfbuzz-2.4.0"
PANGO = "pango-1.42.4"
LQR = "liblqr-1-0.4.2"
XZ = "xz-5.2.4"
TIFF = "tiff-4.0.9"
JBIG = "jbigkit-2.1_macos"
JPEG = "jpeg-9c"
OJPG = "openjpeg-2.3.1"
WEBP = "libwebp-1.0.3"
IM = "ImageMagick-6.9.10-53"

PYCAIRO = "pycairo-1.18.1"
REPORTLAB = "reportlab-3.3.0"
PIL = "Pillow-5.4.1"

# ---------------------------------------------
# Build environment vars
# ---------------------------------------------
os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'
os.environ['CPPFLAGS'] = "-I%s/include" % UC2DIR
os.environ['LDFLAGS'] = "-L%s/lib -arch x86_64" % UC2DIR
os.environ['CFLAGS'] = "-Os -arch x86_64"
os.environ['LD_LIBRARY_PATH'] = "%s/lib" % UC2DIR
os.environ['PATH'] = "%s/bin:" % UC2DIR + os.environ['PATH']
os.environ['PKG_CONFIG'] = "%s/bin/pkg-config" % UC2DIR
os.environ['PKG_CONFIG_PATH'] = "%s/lib/pkgconfig" % UC2DIR
os.environ['PYTHONPATH'] = ':'.join(
    [PY_DIR, os.environ.get('PYTHONPATH', '')])

os.environ['CMAKE_INCLUDE_PATH'] = "%s/include" % UC2DIR
os.environ['CMAKE_LIBRARY_PATH'] = "%s/lib" % UC2DIR
# ---------------------------------------------
# Build
# ---------------------------------------------

os.system('echo "">build.log')

if MAIN_BUILD:
    rm(UC2DIR)

    build(PKGCFG, PREFIX, "--with-internal-glib")
    build(ZLIB, PREFIX)
    build(LIBPNG, PREFIX, TRACK)
    build(FREETYPE, PREFIX, TRACK)
    build(PIXMAN, PREFIX, TRACK)
    build(CAIRO, PREFIX, TRACK, "--disable-xlib")
    build(LCMS, PREFIX)
    build(GETTEXT, PREFIX)
    build(PCRE, PREFIX, "--enable-utf", "--enable-unicode-properties")
    build(FFI, PREFIX)
    build(GLIB, PREFIX)
    build(FONTCFG, PREFIX)
    build(FRIBIDI, PREFIX)
    build(DATRIE, PREFIX)
    build(THAI, PREFIX)
    cmake_build(GRAPH)
    build(HARFBUZZ, PREFIX)
    build(PANGO, PREFIX)
    build(LQR, PREFIX)
    build(XZ, PREFIX)
    build(TIFF, PREFIX)
    jbig_build(JBIG, PREFIX)
    build(JPEG, PREFIX)
    cmake_build(OJPG)
    build(WEBP, PREFIX)
    build(IM, PREFIX)

    # Python packages
    mkdirs(PY_DIR)
    mkdirs(PKG_DIR)
    pycairo_build(PYCAIRO, PREFIX)
    reportlab_build(REPORTLAB)
    pillow_build(PIL)
elif TEST_BUILD:
    pass
elif EXT_BUILD:
    os.environ['ARCHFLAGS'] = '-arch x86_64'
    ext_build('subproj')


echo('\n')
echo('BUILD SUCCESSFUL!', WHITE, eol=True, to_log=True)
