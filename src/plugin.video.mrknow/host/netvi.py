# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - netvi"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,pCommon,settings

log = pLog.pLog()

mainUrl = 'http://netvi.pl/'
catUrl = 'https://watch.netvi.tv/api/channels/list'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

class netvi:
    def __init__(self):
        log.info('Starting netvi.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "netvi.cookie"
    def login(self):    
        if ptv.getSetting('netvi.pl_login') == 'true':
            post_data = {'login': ptv.getSetting('netvi.pl_user'), 'password': ptv.getSetting('netvi.pl_pass')}
            query_data = {'url': 'https://watch.netvi.tv/login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            #print ("Data1",data)
            query_data = {'url': 'https://watch.netvi.tv/login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            #print ("Data2",data)
            if self.isLoggedIn(data) == True:
                xbmc.executebuiltin("XBMC.Notification(" + ptv.getSetting('netvi.pl_user') + ", Zostales poprawnie zalogowany,4000)")
            else:
                xbmc.executebuiltin("XBMC.Notification(Błędny login i hasło do serwisu, Wpisz poprawne dane w ustawieniach,4000)") 
                self.settings.showSettings()
                
        else:
            log.info('Wyświetlam ustawienia')
            xbmc.executebuiltin("XBMC.Notification(Brak loginu i hasla, Wpisz login i haslo w ustawieniach,4000)") 
            self.settings.showSettings()
            
    def isLoggedIn(self, data):
        #print data
        lStr = '<a href="/logout">Wyloguj</a>'
        if lStr in data:
          return True
        else:
          return False


    def listsCategoriesMenu(self):
        query_data = { 'url': catUrl, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        #match = re.compile('<ul class="select-movie-type movie-kat-selection">(.*?)</ul>', re.DOTALL).findall(link)
        #match1 = re.compile('<a href="#" rel="filter" type="kat" value="(.*?)" >&#9632; (.*?)</a>', re.DOTALL).findall(match[0])
        print link
        json_object = json.loads(link)
        print json_object
        for chanel in json_object['channels']:   
            print chanel['name']
            log.info('Listuje kanały: ')
            self.add('netvi', 'playSelectedMovie', 'None', chanel['name'],chanel['thumbnail'], 'https://watch.netvi.tv/api/channels/get/'+chanel['id']+'?format_id=1', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getMovieLinkFromXML(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        json_object = json.loads(link)
        print json_object

        if json_object['status'] == 'ok':
            url = json_object['stream_channel']['url_base']
            print ("url",url)
            query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            print link
            match = re.compile('<media url="(.*?)" bitrate="(.*?)"/>', re.DOTALL).findall(link)
            match1 = re.compile('<baseURL>(.*?)</baseURL>', re.DOTALL).findall(link)
            #
            
            print "jest OK"
            tab = []
            for i in range(len(match)):
                tab.append('Bitrate - '+match[i][1])
            d = xbmcgui.Dialog()        
            video_menu = d.select("Wybór jakości video", tab)
            #rtmpdump -r "rtmp://w-stream2.4vod.tv:1935/3/_definst_" -a "3/_definst_" -f "WIN 11,6,602,180" -W "https://watch.netvi.tv/javascripts/libs/flowplayer/flowplayer.commercial-3.2.11.swf" -p "https://watch.netvi.tv/" --live -C S:a28777a987ae7d30e252fb07493e9054 -C S:Hxzqq96TqcvzFO61Kl2xq4RimcruUu3X -y "mp4:33.stream" -o mp4_33.stream.flv
#            link = 'rtmp://w-stream3.4vod.tv:1935/3/_definst_ app=3/_definst_ swfUrl=https://watch.netvi.tv/javascripts/libs/flowplayer/flowplayer.commercial-3.2.11.swf pageUrl=https://watch.netvi.tv/ live=true conn=S:'+json_object['stream_channel']['url_params'][1]+' conn=S:'+json_object['stream_channel']['url_params'][2]+' playpath='+match[0]
            if video_menu > -1:
                link = match1[0]+' app='+json_object['stream_channel']['channel_id']+'/_definst_ swfUrl=https://watch.netvi.tv/javascripts/libs/flowplayer/flowplayer.commercial-3.2.11.swf pageUrl=https://watch.netvi.tv/ live=true conn=S:'+json_object['stream_channel']['url_params'][1]+' conn=S:'+json_object['stream_channel']['url_params'][2]+' playpath='+match[video_menu][0]
                return link
            else:
                return False
        else:
            return False 
 
    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True, strona = '', img = ''):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&strona=" + urllib.quote_plus(strona)+ "&img=" + urllib.quote_plus(img)
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
        liz.setInfo( type = "Video", infoLabels={ "Title": title, } )
        try:
            xbmcPlayer = xbmc.Player()
            #xbmcPlayer.play(videoUrl+'|Referer=https://watch.netvi.tv/javascripts/libs/flowplayer/flowplayer.commercial-3.2.11.swf', liz)
            xbmcPlayer.play(videoUrl, liz)
            
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
        img = self.parser.getParam(params, "img")
        #print ("DANE",url,title,strona)
        
        
        if name == None:
            self.login()
            self.listsCategoriesMenu()
        elif name == 'main-menu' and category == 'Alfabetycznie':
            log.info('Jest Alfabetycznie: ')
            self.listsItemsA(catUrl)
        elif name == 'page-menu' and category == 'None':
            log.info('Jest Alfabetycznie Litera: '+ title)
            self.listsItemsS(catUrl,title)
        elif name == 'serial-menu' and category == 'None':
            log.info('Jest Serial Menu: ')
            self.listsSeasons(url)
        elif name == 'items-menu' and category == 'None':
            log.info('Jest Sezon: '+strona)
            self.listsItems(url,strona)
        elif name == 'main-menu' and category == 'Top 30':
            log.info('Jest Top 30: ')
            self.listsItemsTop(catUrl,'TOP 30','Ostatnie dodane seriale')
        elif name == 'main-menu' and category == 'Ostatnie dodane seriale':
            self.listsItemsTop(catUrl,'Ostatnie dodane seriale', 'Ostatnie dodane odcinki')
        elif name == 'main-menu' and category == 'Ostatnie dodane odcinki':
            log.info('Jest Gorące: ')
            self.listsItemsOst(catUrl)
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            if key != None:
                self.listsItemsOther(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url,strona,filtrowanie)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
