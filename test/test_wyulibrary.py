# -*- coding: utf-8 -*-

from service.wyulibrary import WyuLibrary

if __name__ == '__main__':
    lib = WyuLibrary()
    print lib.search_book("java")