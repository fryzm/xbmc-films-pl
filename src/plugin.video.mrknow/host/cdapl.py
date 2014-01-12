# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,urlparse
import json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - cda.pl"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, libCommon, Parser

log = pLog.pLog()

mainUrl = 'http://cda.pl/'
movies = 'http://www.cda.pl/video/show/ca%C5%82e_filmy_or_ca%C5%82y_film_or_lektor_or_dubbing_or_napisy/p3?'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Filmy najtrafniejsze",
            2: "Filmy najwyżej ocenione",
            3: "Filmy popularne",
            4: "Filmy najnowsze",
            5: "Filmy alfabetycznie",
            6: "Najnowsze",
            7: "Video najpopularniejsze na FB",
            8: "Video najlepiej ocenione",
            9: "Krótkie filmy i animacje",
            10: "Filmy Extremalne",
            11: "Motoryzacja, wypadki",
            12: "Muzyka",
            13: "Prosto z Polski",
            14: "Rozrywka",
            15: "Różności",
            16: "Sport",
            17: "Śmieszne filmy",
            
            27: "Szukaj"            }

max_stron = 0            

class cdapl:
    def __init__(self):
        log.info('Starting cdapl.pl')
        self.cm = libCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('cdapl', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsCategoriesMenu(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #ile jest filmów ?
        match = re.compile('<li class="active"id="mVid"><a href="#" onclick="moreVideo\(\);return false;">Video \((.*?)\)</a></li>', re.DOTALL).findall(link)
        ilejest = int(match[0])
        policz = int(ilejest/o_filmow_na_stronie) +1
        max_stron = policz
        parsed = urlparse.urlparse(url)
        typ = urlparse.parse_qs(parsed.query)['s'][0]
        for i in range(0, (policz)):
            purl = 'http://www.cda.pl/video/show/ca%C5%82e_filmy_or_ca%C5%82y_film/p'+str(i+1)+'?s='+typ
            self.add('cdapl', 'categories-menu', 'Strona '+str(i+1), 'None', 'None', purl, 'None', 'None', True, False,str(i+1))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = 'http://www.cda.pl/video/show/' + urllib.quote_plus(key) +'//p1?s=best'
        #http://www.cda.pl/video/show/xxx/p2?s=best
        return url

    def listsItems(self, url):
        print ("URL",url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #match = re.compile('<label  title="(.*?)"> (.*?)</label>', re.DOTALL).findall(link)
        match = re.compile('<div class="thumbElem video_(.*?)">(.*?)</label>', re.DOTALL).findall(link)
        #<div class="videoElem">
        
        print ("Match",match)
        if len(match) > 0:
            for i in range(len(match)):
                print ("Match ->I",match[i])
            
                match1 = re.compile('<img height="90" width="120" src="(.*?)" alt="(.*?)">\n<span class="timeElem">\n(.*?) </span>\n</a>\n<div class="text">\n<a class="titleElem" href="(.*?)">(.*?)</a>', re.DOTALL).findall(link)
                print (match1)
                self.add('cdapl', 'playSelectedMovie', 'None', match1[i][4] +' - ' + match1[i][2], match1[i][0], mainUrl+match1[i][3], 'aaaa', 'None', True, False)
        else:
            match2 = re.compile('<div class="block upload" id="dodane_video">(.*?)<div class="paginationControl">', re.DOTALL).findall(link)
            match3 = re.compile('<div class="videoElem">\n                  <a href="(.*?)" style="position:relative;width:120px;height:90px" title="(.*?)">\n                    <img width="120" height="90" src="(.*?)" title="(.*?)" alt="(.*?)" />\n ', re.DOTALL).findall(match2[0])
            if len(match3) > 0:
                for i in range(len(match3)):
                    self.add('cdapl', 'playSelectedMovie', 'None', self.cm.html_special_chars(match3[i][1]) , match3[i][2], mainUrl+match3[i][0], 'aaaa', 'None', True, False)

        match10 = re.compile('<span class="next-wrapper"><a onclick="javascript:changePage\((.*?)\);return false;" class="sbmBigNext btn-my btn-large fiximg" href="(.*?)">(.*?)></a></span>', re.DOTALL).findall(link)
        if len(match10) > 0:
            self.add('cdapl', 'categories-menu', 'Następna strona', 'None', 'None', mainUrl+match10[0][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItems2(self, url):
        print ("URL",url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #match = re.compile('<div class="videoElem"> <a class="aBoxVideoElement" style="position: relative; relative" href="(.*?)" title="(.*?)"  style="position: relative;width: 120px; height: 90px;"> <img width="120" height="90" src="(.*?)" class="block"/>', re.DOTALL).findall(link)
        #<div class="videoElem"> <a class="aBoxVideoElement" style="position: relative; relative" href="/video/107593a9/GTA-6-Rosja" title="GTA 6: Rosja" style="position: relative;width: 120px; height: 90px;"> <img width="120" height="90" src="http://img3.cda.pl/f529e45c402508f7ab115db346c559b0/13883673668120-01.jpg" class="block"/>
        match = re.compile('<div class="videoElem"> <a class="aBoxVideoElement" style="(.*?)" href="(.*?)" title="(.*?)" style="(.*?)"> <img width="120" height="90" src="(.*?)" class="block"/>', re.DOTALL).findall(link)
        
        print ("Match",match)
        print ("Match",self.cm.html_special_chars("ALAL"))
        
        if len(match) > 0:
            for i in range(len(match)):
                #self.add('cdapl', 'playSelectedMovie', 'None', self.cm.html_special_chars(match[i][2]) , match[i][4], mainUrl+match[i][1], 'aaaa', 'None', True, False)
                self.add('cdapl', 'playSelectedMovie', 'None', match[i][2] , match[i][4], mainUrl+match[i][1], 'aaaa', 'None', True, False)

        match10 = re.compile('<span class="next-wrapper"><a onclick="javascript:changePage\((.*?)\);return false;" class="sbmBigNext btn-my btn-large fiximg" href="(.*?)">(.*?)></a></span>', re.DOTALL).findall(link)
        if len(match10) > 0:
            self.add('cdapl', 'main-menu', 'Następna strona', 'None', 'None', mainUrl+match10[0][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getMovieLinkFromXML(self, url):
        return self.up.getVideoLink(url)

  

    def getMovieID(self, url):
        id = 0
        tabID = url.split(',')
        if len(tabID) > 0:
            id = tabID[1]
        return id


    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[1])
        return out

    def getItemURL(self, table, key):
        link = ''
        for i in range(len(table)):
            value = table[i]
            if key in value[0]:
                link = value[2]
                break
        return link


    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,strona=''):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&strona=" + urllib.quote_plus(strona)
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
            

    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon):
        ok=True
        if videoUrl == '':
                d = xbmcgui.Dialog()
                d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
                return False
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": title, } )
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl+"|Referer=http://static.cda.pl/player5.9/player.swf", liz)
            
            if not xbmc.Player().isPlaying():
                xbmc.sleep( 10000 )
                #xbmcPlayer.play(url, liz)
            
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu.', 'Problem')        
        return ok


    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        strona = self.parser.getParam(params, "strona")
        print ("Dane",name,category,title)
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Najnowsze':
            self.listsItems2('http://www.cda.pl/video/p1')
        elif name == 'main-menu' and category == 'Video najpopularniejsze na FB':
            self.listsItems2('http://www.cda.pl/video/p1?o=popular&k=miesiac')
        elif name == 'main-menu' and category == 'Video najlepiej ocenione':
            self.listsItems2('http://www.cda.pl/video/p1?o=top&k=miesiac')
        elif name == 'main-menu' and category == 'Krótkie filmy i animacje':
            self.listsItems2('http://www.cda.pl/video/kat26/p1')
        elif name == 'main-menu' and category == 'Filmy Extremalne':
            self.listsItems2('http://www.cda.pl/video/kat24/p1')
        elif name == 'main-menu' and category == 'Motoryzacja, wypadki':
            self.listsItems2('http://www.cda.pl/video/kat27/p1')
        elif name == 'main-menu' and category == ' Muzyka':
            self.listsItems2('http://www.cda.pl/video/kat28/p1')
        elif name == 'main-menu' and category == 'Prosto z Polski':
            self.listsItems2('http://www.cda.pl/video/kat29/p1')
        elif name == 'main-menu' and category == 'Rozrywka':
            self.listsItems2('http://www.cda.pl/video/kat30/p1')
        elif name == 'main-menu' and category == 'Różności':
            self.listsItems2('http://www.cda.pl/video/kat33/p1')
        elif name == 'main-menu' and category == 'Sport':
            self.listsItems2('http://www.cda.pl/video/kat31/p1')
        elif name == 'main-menu' and category == 'Śmieszne filmy':
            self.listsItems2('http://www.cda.pl/video/kat32/p1')            
        elif name == 'main-menu' and category == 'Następna strona':
            self.listsItems2(url)   
            
        elif name == 'main-menu' and category == 'Filmy najtrafniejsze':
            log.info('Jest Najtrafniejsze: ')
            self.listsItems(movies +'s=best')
        elif name == 'main-menu' and category == 'Filmy najwyżej ocenione':
            log.info('Jest Najwyżej ocenione: ')
            self.listsItems(movies +'s=rate')
        elif name == 'main-menu' and category == 'Filmy popularne':
            log.info('Jest Popularne: ')
            self.listsItems(movies +'s=popular')
        elif name == 'main-menu' and category == 'Filmy najnowsze':
            log.info('Jest Najnowsze: ')
            self.listsItems(movies +'s=date')
        elif name == 'main-menu' and category == 'Filmy alfabetycznie':
            log.info('Jest Alfabetycznie: ')
            self.listsItems('s=alf')
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            if key != None:
                self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category == 'filmy':
            log.info('url: ' + str(movies))
            self.listsItems(movies)
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            log.info('strona: ' + str(strona))
            self.listsItems(url)            
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
