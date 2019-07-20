# -*- coding: utf-8 -*-
#
#   Build utils for UniConvertor 2.x on macOS
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

from config import *

# ---------------------------------------------
# Color vars
# ---------------------------------------------
GREEN = "\033[0;92m"
YELLOW = "\033[0;93m"
RED = "\033[0;41m"
CYAN = "\033[0;96m"
WHITE = "\033[0;97m"
NC = "\033[0m"
NCE = "\033[0m\n"
TR = '\n' + '-' * 45 + '\n'

shift = ''


# ---------------------------------------------
# Build functions
# ---------------------------------------------
def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_log_header(msg):
    os.system('printf "\n%s%s %s" %s' % (TR, msg, TR, LOG))


def echo(message='', color=GREEN, eol=False, to_log=False):
    message = message
    if to_log:
        write_log_header(message)
    if not VERBOSE:
        msg = [color] if color else []
        msg += [message, NCE if eol else NC]
        os.system('printf "%s"' % ''.join(msg))


def resolve_cmd(cmd):
    if cmd.startswith('./configure'):
        return 'configure'
    elif cmd.startswith('rm '):
        return 'deleting ' + ' '.join(cmd.split()[2:])
    elif cmd.startswith('tar '):
        return 'unpacking ' + ' '.join(cmd.split()[2:])
    elif cmd.startswith('mv '):
        return 'moving to ' + cmd.split()[2]
    elif cmd.startswith('cp '):
        return 'copying to ' + cmd.split()[-1]
    else:
        return cmd


def run_decorator(func):
    def run_decorator_inner(cmd, *args):
        echo(shift + resolve_cmd(cmd), eol=False)
        echo('..', eol=False)
        func(cmd, *args)
        echo('..', eol=False)
        echo('[  OK  ]', eol=True)

    return run_decorator_inner


@run_decorator
def run(cmd):
    cmd = cmd + LOG
    if os.system(cmd):
        echo('[ FAIL ]', RED, True)
        raise RuntimeError


def rm(path):
    if not os.path.exists(path):
        return
    try:
        run('rm -rf %s' % path)
    except RuntimeError:
        echo(message='BUILD FAILED! See reason in build.log',
             color=YELLOW, eol=True, to_log=True)
        sys.exit(1)


def build_decorator(func):
    def build_decorator_inner(libname, *args):
        echo('Building %s ' % libname, CYAN, eol=True, to_log=True)
        global shift
        shift = ' ' * 4
        if func(libname, *args):
            shift = ''
            echo(message='BUILD FAILED! See reason in build.log',
                 color=YELLOW, eol=True, to_log=True)
            sys.exit(1)
        shift = ''
        return

    return build_decorator_inner


def catcher(func):
    def catcher_inner(libname, *args):
        try:
            ret = func(libname, *args)
        except RuntimeError:
            ret = True
        finally:
            os.chdir(CUR_DIR)
            rm(libname)
        return ret

    return catcher_inner


@build_decorator
@catcher
def build(libname, *args):
    run('tar -xzf src/%s.tar.gz' % libname)
    os.chdir(libname)
    run('./configure %s' % ' '.join(args))
    run('make')
    run('make install')


@build_decorator
@catcher
def py_build(libname, *args):
    run('tar -xzf src/%s.tar.gz' % libname)
    os.chdir(libname)
    run('python setup.py build')
    run('python setup.py install %s' % ' '.join(args))


def pycairo_build(libname, *args):
    py_build(libname, *args)
    if any([item.startswith(libname) for item in os.listdir(PY_DIR)]):
        cairo_egg_dir = [item for item in os.listdir(PY_DIR)
                         if item.startswith(libname)][0]
        cairo_egg_dir = os.path.join(PY_DIR, cairo_egg_dir)
        cairo_inc = '%s/cairo/include' % cairo_egg_dir
        os.system('mv %s %s/cairo/pycairo' % (cairo_inc, cairo_egg_dir))
        os.system('mv %s/cairo/pycairo %s/include' % (cairo_egg_dir, UC2DIR))
        os.system('mv %s/cairo %s' % (cairo_egg_dir, PKG_DIR))
        echo('\n', to_log=True)
        rm(cairo_egg_dir)


@build_decorator
@catcher
def reportlab_build(libname, *_args):
    run('tar -xzf src/%s.tar.gz' % libname)
    run('mv reportlab %s' % PKG_DIR)


@build_decorator
@catcher
def jbig_build(libname, *_args):
    run('tar -xzf src/%s.tar.gz' % libname)
    os.chdir(libname)
    run('cp -R libjbig/lib*.* %s/lib' % UC2DIR)
    run('cp libjbig/*.h %s/include' % UC2DIR)
    os.chdir(CUR_DIR)
    rm(libname)


@build_decorator
@catcher
def cmake_build(libname, *_args):
    run('tar -xzf src/%s.tar.gz' % libname)
    os.chdir(libname)
    run('mkdir build')
    os.chdir('build')
    run('cmake .. -DCMAKE_BUILD_TYPE=Release '
        '-DCMAKE_INSTALL_PREFIX="%s"' % UC2DIR)
    run('make')
    run('make install')


@build_decorator
@catcher
def pillow_build(libname, *args):
    run('tar -xzf src/%s.tar.gz' % libname)
    os.chdir(libname)
    if not os.path.exists(PY_DIR):
        os.makedirs(PY_DIR)
    run('MAX_CONCURRENCY=1 python setup.py build_ext '
        '--enable-zlib --enable-jpeg --enable-tiff --enable-freetype '
        '--enable-lcms --enable-webp --enable-jpeg2000 '
        '--disable-imagequant install --prefix %s' % UC2DIR)
    pil_egg = [item for item in os.listdir(PY_DIR)
               if item.startswith(libname)]
    if pil_egg:
        pil_egg = os.path.join(PY_DIR, pil_egg[0])
        run('unzip %s -d %s' % (pil_egg, PKG_DIR))
        rm(PY_DIR)
        egg_info = os.path.join(PKG_DIR, 'EGG-INFO')
        rm(egg_info)
