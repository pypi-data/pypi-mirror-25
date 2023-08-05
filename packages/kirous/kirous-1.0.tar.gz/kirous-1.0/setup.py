#!/usr/bin/env python3

from distutils.core import setup, Extension

kirous_sources = [
    'src/core/error.c',
    'src/core/util.c',
    
    'src/core/screen.c',
    'src/core/colors.c',
    'src/core/keyboard.c',
    
    'src/core/backend_curses.c',
    'src/core/backend_dummy.c',
    'src/core/backend_opengl.c',
    'src/core/backend_serial.c',
    
    'src/pywrap/pyscreenwrapper.c',
    'src/pywrap/pycolorwrapper.c',
    'src/pywrap/pykeyboardwrapper.c',
    'src/pywrap/pywrapper.c'
]

kirous = Extension('kirous',
                    define_macros=[('OPENGL_SUPPORT', '1'),
                                   ('_XOPEN_SOURCE_EXTENDED', '1')],
                    sources=kirous_sources,
                    libraries=['ncursesw', 'X11', 'GL'],
                    extra_compile_args=['-std=gnu11'])

def main():
    setup(name='kirous',
        version='1.0',
        description='',
        author = 'eichkat3r',
        author_email = 'mail@katerbase.de',
        ext_modules=[kirous]
    )

if __name__ == '__main__':
    main()
