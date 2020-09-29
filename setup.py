from distutils.core import setup, Extension
 
module = Extension('calculation', sources = ['calculation.c'])
 
setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a package for calculation',
        ext_modules = [module])