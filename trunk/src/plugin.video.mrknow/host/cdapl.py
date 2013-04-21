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

import pLog, pCommon, Parser

log = pLog.pLog()

mainUrl = 'http://cda.pl/'
movies = 'http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=best&section=vid'
moovie_news = 'http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=date&section=vid'
#alfabetycznie - http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=alf&section=vid
#naj ocenione - http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=rate&section=vid
#popularne http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=popular&section=vid
#najnowsze http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=date&section=vid
#najtrafniejsze http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=best&section=vid

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

o_filmow_na_stronie = 65

MENU_TAB = {#1: "Najtrafniejsze",
            2: "Najwyżej ocenione",
            3: "Popularne",
            4: "Najnowsze",
            5: "Alfabetycznie",
            6: "Szukaj",
            }

max_stron = 0            

class cdapl:
    def __init__(self):
        log.info('Starting cdapl.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()

    def getstring(self,data):
        data = data.replace('&oacute;','ó').replace('&Oacute;','Ó')
        #data = data.replace('\u017c','ż').replace('\u017b','Ż')
        return data
        
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
        url = 'http://www.cda.pl/info/' + urllib.quote_plus(key) 
        return url

    def listsItems(self, url,strona):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<li id="mVid"><a href="#" onclick="moreVideo\(\);return false;">Video \((.*?)\)</a></li>', re.DOTALL).findall(link)
        match1 = re.compile('<img height="90" width="120" src="(.*?)" \r\n    alt="(.*?)">\r\n     \r\n    <span class="timeElem">\r\n(.*?)</span>\r\n    </a>\r\n  <div class="text"> \r\n    <a class="titleElem" title="(.*?)" href="(.*?)">(.*?)</a>', re.DOTALL).findall(link)
        
        if len(match1) > 0:
            for i in range(len(match1)):
                self.add('cdapl', 'playSelectedMovie', 'None', self.getstring(match1[i][1]) +' - ' + match1[i][2], match1[i][0], mainUrl+match1[i][4], 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItemsPage(self, url):
        if not url.startswith("http://"):
            url = mainUrl + url
        if self.getSizeAllItems(url) > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(self.getSizeAllItems(url)) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('cdapl', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def listsItemsSerialPage(self, url, sizeOfSerialParts):
        if not url.startswith("http://"):
            url = mainUrl + url
        if sizeOfSerialParts > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(sizeOfSerialParts) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('cdapl', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, url):
        return self.up.getVideoLink(url)


    def getSizeAllItems(self, url):
        numItems = 0
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<li data-theme="c" action="watch">(.*?)<a href="(.*?)" data-transition="slide">(.*?)<img src="(.*?)" height="90px" width="90px" title="(.*?)" />(.*?)</a>(.*?)</li>', re.DOTALL).findall(readURL)
        if len(match) == 1:
            numItems = match[0]
        return numItems
    
    
    def getSizeItemsPerPage(self, url):
        numItemsPerPage = 0
        openURL = urllib.urlopen(url)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<div class="movie-(.+?)>').findall(readURL)
        if len(match) > 0:
            numItemsPerPage = len(match)
        return numItemsPerPage        

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
        
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Najtrafniejsze':
            log.info('Jest Najtrafniejsze: ')
            self.listsCategoriesMenu('http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=best&section=vid')
        elif name == 'main-menu' and category == 'Najwyżej ocenione':
            log.info('Jest Najwyżej ocenione: ')
            self.listsCategoriesMenu('http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=rate&section=vid')
        elif name == 'main-menu' and category == 'Popularne':
            log.info('Jest Popularne: ')
            self.listsCategoriesMenu('http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=popular&section=vid')
        elif name == 'main-menu' and category == 'Najnowsze':
            log.info('Jest Najnowsze: ')
            self.listsCategoriesMenu('http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=date&section=vid')
        elif name == 'main-menu' and category == 'Alfabetycznie':
            log.info('Jest Alfabetycznie: ')
            self.listsCategoriesMenu('http://www.cda.pl/info/ca%C5%82e_filmy_or_ca%C5%82y_film?s=alf&section=vid')
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            if key != None:
                self.listsItems(self.getSearchURL(key),0)
        elif name == 'categories-menu' and category == 'filmy':
            log.info('url: ' + str(movies))
            self.listsItems(movies)
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            log.info('strona: ' + str(strona))
            self.listsItems(url,strona)            
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
