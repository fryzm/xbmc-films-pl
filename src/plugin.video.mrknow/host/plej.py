# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser
import json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - plej"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, pCommon, Parser, settings

log = pLog.pLog()

mainUrl = 'http://plej.tv/'
chanels = 'http://plej.tv/index.php?p=kanal'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Wszystkie",
            3: "Szukaj" }


class plej:
    def __init__(self):
        log.info('Starting plej.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.settings = settings.TVSettings()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "plej.cookie"
        
    def login(self):    
        if ptv.getSetting('plej_login') == 'true':
            post_data = {'login': ptv.getSetting('plej_user'), 'pass': ptv.getSetting('plej_pass'), 'log_in2':'Zaloguj'}
            query_data = {'url': mainUrl+'index.php?p=login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            #print ("Data1",data)
            #post_data = {'login': ptv.getSetting('plej_user'), 'pass': ptv.getSetting('plej_pass'), 'log_in2':'Zaloguj'}
            #query_data = {'url': mainUrl+'index.php?p=login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            #data = self.cm.getURLRequestData(query_data, post_data)
            #print ("Data2",data)
            if self.isLoggedIn(data) == True:
                xbmc.executebuiltin("XBMC.Notification(" + ptv.getSetting('plej_user') + ", Zostales poprawnie zalogowany,4000)")
            else:
                xbmc.executebuiltin("XBMC.Notification(Blad logowania, uzywam Player z limitami,4000)")  
        else:
            log.info('Wyświetlam ustawienia')
            #self.settings.showSettings()
            xbmc.executebuiltin("XBMC.Notification(Skonfiguruj konto w ustawieniach, obecnie uzywam Player z limitami,4000)")  
            
    def isLoggedIn(self, data):
        lStr = '<li><a class="play" href="index.php?p=logout" title="" >WYLOGUJ</a></li>'
        if lStr in data:
          return True
        else:
          return False

    def listsMainMenu(self, table):
        query_data = { 'url': chanels, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<table style="width:100%"><tr><td style="width:30%;vertical-align:middle;"><a href="(.*?)" title="(.*?)"><img style="width:50px;height:40px;" src="(.*?)" alt="" /></a></td>', re.DOTALL).findall(link)
        #print match
        for o in range(len(match)):
            #if self.getMovieType(mainUrl+match[o][0]) == True:
                #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                #self.add('plej', 'playSelectedMovie', 'None', nazwa, mainUrl+image, stream, 'None', 'None', True, False)
                self.add('plej', 'playSelectedMovie', 'None', match[o][1], mainUrl+match[o][2], mainUrl+match[o][0], 'None', 'None', True, False)
            #else:
            #    self.add('plej', 'items-menu', 'None', match[o][1], mainUrl+match[o][2], mainUrl+match[o][0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<table style="width:100%"><tr><td style="width:30%;vertical-align:middle;"><a href="(.*?)" title="(.*?)"><img style="width:50px;height:40px;" src="(.*?)" alt="" /></a></td>', re.DOTALL).findall(readURL)
        #print match
        if len(match) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match)):
                url = mainUrl + match[i][1]
                self.add('plej', 'categories-menu', match[i][2].strip(), 'None', 'None', url, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        

    def listsItems(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile("\n            'playlist':(.*?)'autostart': 'true',",re.DOTALL).findall(link)
        print ("LINK",match)
        match1 = re.compile('{"file":"(.*?)"}],"title":"(.*?)"}', re.DOTALL).findall(match[0])
        print ("Match1",match1)
        #linkVideo = self.up.getVideoLink(match[0])
        for i in range(len(match1)):
            self.add('plej', 'playYoutube', 'None', str(i) +'. ' +match1[i][1], 'None', self.up.getVideoLink(match1[i][0].replace('\\','')), 'aaaa', 'None', True, True)

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
                self.add('plej', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
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
                self.add('plej', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 

    def getMovieType(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('src: "(.*?)",', re.DOTALL).findall(link)
        match1 = re.compile('streamer  : \'(.*?)\',', re.DOTALL).findall(link)
        #print ("ZZZZZZZZ",match,url,link)
        if len(match)>0:
            return True
        elif len(match1)>0:
            return True
        else:
            return False
        
    def getMovieLinkFromXML(self, url):
        #print ("URL",url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('src: "(.*?)",', re.DOTALL).findall(link)
        match1 = re.compile('streamer  : \'(.*?)\',', re.DOTALL).findall(link)
        #print ("AAAAAAAAAAAAAA",match,url,link)
        if len(match)>0:
            linkVideo = match[0]
            return linkVideo
        if len(match1)>0:
            match2 = re.compile('video     : \'(.*?)\',', re.DOTALL).findall(link)
            linkVideo = match1[0] + '/'+match2[0]
            return linkVideo
        

    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
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
            xbmcPlayer.play(videoUrl, liz)
            
           # if not xbmc.Player().isPlaying():
           #     xbmc.sleep( 10000 )
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
        print(name,category,url,title)
        if name == None:
            self.login()
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Wszystkie':
            log.info('Jest Wszystkie: ')
            self.listsCategoriesMenu(chanels)
            
        elif name == 'items-menu':
            key = self.searchInputText()
            self.listsItems(url)
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            if self.getMovieType(url) == True:
                self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)
            else:
                self.listsItems(url)
        if name == 'playYoutube':
                self.LOAD_AND_PLAY_VIDEO(url, title, icon)
        
  
