# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser
import json,hashlib


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - wrzuta"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, pCommon, Parser, settings

log = pLog.pLog()

mainUrl = 'http://www.wrzuta.pl/'
catUrl = mainUrl + 'ajax/pliki/edytuj'
loginUrl = 'https://ssl.wrzuta.pl/zaloguj'


HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Wszystkie",
            2: "Moje",
            3: "Szukaj" }


class wrzuta:
    def __init__(self):
        log.info('Starting wrzuta.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.settings = settings.TVSettings()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wrzuta.cookie"

    def login(self):    
        if ptv.getSetting('wrzuta_login') == 'true':
            
            tmplogin = hashlib.sha1(ptv.getSetting('wrzuta_pass')).hexdigest()
            tmplogin1 = hashlib.sha1(tmplogin+ptv.getSetting('wrzuta_user')).hexdigest()
            query_data = { 'url': loginUrl, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }        
            link = self.cm.getURLRequestData(query_data)
            print ("L",link)
            post_data = {'login': ptv.getSetting('wrzuta_user'), 'password': tmplogin1, 'user_remember':'','fbid': ''}
            #login=mrknow&password=ffcee7d644dab355cb9111ceb96c348786fe9a82&user_remember=&fbid=
            
            query_data = {'url': loginUrl, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            print ("Data1",data)
            #post_data = {'login': ptv.getSetting('wrzuta_user'), 'pass': ptv.getSetting('wrzuta_pass'), 'log_in2':'Zaloguj'}
            #query_data = {'url': mainUrl+'index.php?p=login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            #data = self.cm.getURLRequestData(query_data, post_data)
            #print ("Data2",data)
            if self.isLoggedIn(data) == True:
                xbmc.executebuiltin("XBMC.Notification(" + ptv.getSetting('wrzuta_user') + ", Zostales poprawnie zalogowany,4000)")
            else:
                xbmc.executebuiltin("XBMC.Notification(Blad logowania,4000)")  
        else:
            log.info('Wyświetlam ustawienia')
            #self.settings.showSettings()
            xbmc.executebuiltin("XBMC.Notification(Skonfiguruj konto w ustawieniach, obecnie uzywam Player z limitami,4000)")  
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('wrzuta', 'main-menu', val, val, 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    def listsCategoriesMenu(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)

        print link
        
        print len(match)
        print match
        
        if len(match) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match)):
                url = self.mainUrl + match[i][0]
                self.add('noobroom', 'categories-menu', match[i][1].strip(), 'None', 'None', url, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        

    def listsCategoriesMy(self):
        self.login()
        query_data = { 'url': mainUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)

        print ("Link",link)
        match = re.compile('<p class="user-box-name"><a href="(.*?)">(.*?)</a></p>', re.DOTALL).findall(link)

        print len(match)
        print match
        
        if len(match) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match)):
                url = self.mainUrl + match[i][0]
                self.add('noobroom', 'categories-menu', match[i][1].strip(), 'None', 'None', url, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
        
    def getMovieLinkFromXML(self, url):
        #print ("URL",url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile("file: '(.*?)',", re.DOTALL).findall(link)
        #print ("AAAAAAAAAAAAAA",match,url,link)
        if len(match)>0:
            linkVideo = match[0]
            linkVideo = linkVideo + ' pageUrl='+url+' swfUrl=http://wrzuta.tv/jwplayer/jwplayer.flash.swf'
            return linkVideo
        else:
            return False
        

    

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
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Kategorie':
            log.info('Jest Kategorie: ')
            self.listsCategoriesMenu(catUrl)
        elif name == 'main-menu' and category == 'Moje':
            log.info('Jest Moje: ')
            self.listsCategoriesMy()            
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)
        
  
