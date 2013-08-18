# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon



scriptID = 'plugin.video.xbmcfilm'
scriptname = "Films online"
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, Parser, pCommon
import json

log = pLog.pLog()


mainUrl = 'http://xbmcfilm.com/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Aktualnie oglądane",
            2: "Najczęściej oglądane - 7 dni",
            3: "Najczęściej oglądane - 30 dni",
            4: "Najczęściej oglądane"


            }


class xbmcfilm:
    def __init__(self):
        log.info('Starting xbmcfilm.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.cm = pCommon.common()
        self.settings = settings.TVSettings()


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('cdapl', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def listsItems(self, url):
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #print ("L",link)
        #objs = json.loads(link)
        objs = json.loads(link)    

        for o in objs[0]:
            #print o
            nazwa = json.dumps(o["title"]).replace('"','')
        #    print nazwa
            stream = json.dumps(o["xbmcpath"]).replace('"','')
            image = json.dumps(o["image"]).replace('"','')

        #    image = ptv.getAddonInfo('path') + os.path.sep + "images" + os.path.sep  + nazwa +".png"
            
            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
            #self.add('mmtv', 'playSelectedMovie', 'None', nazwa, mainUrl+image, stream, 'None', 'None', True, False)
            self.add('xbmcfilm', 'playSelectedMovie', 'None', nazwa.decode('utf-8'),image, stream, 'None', 'None', True, False)
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
       
    

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
        print ("videurl", videoUrl)
        print ("videurl", videoUrl)
 
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
        elif name == 'main-menu' and category == 'Aktualnie oglądane':
            self.listsItems('http://xbmcfilm.com/index.php/xbmc/')
        elif name == 'main-menu' and category == 'Najczęściej oglądane':
            self.listsItems('http://xbmcfilm.com/index.php/xbmc/mostwatched')
        elif name == 'main-menu' and category == 'Najczęściej oglądane - 30 dni':
            self.listsItems('http://xbmcfilm.com/index.php/xbmc/mostwatched/30')
        elif name == 'main-menu' and category == 'Najczęściej oglądane - 7 dni':
            self.listsItems('http://xbmcfilm.com/index.php/xbmc/mostwatched/7')
        

        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(url, title, icon)
        
  
init = xbmcfilm()
init.handleService()