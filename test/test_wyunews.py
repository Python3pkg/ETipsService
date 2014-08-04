# -*- coding: utf-8 -*-

from service.wyunews import WyuNews

if __name__ == '__main__':
    wyunews = WyuNews()
    print (wyunews.get_wyu_news(1))