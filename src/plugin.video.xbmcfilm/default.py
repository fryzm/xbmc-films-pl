# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon



ptv = xbmcaddon.Addon()
scriptID = ptv.getAddonInfo('id')
scriptname = ptv.getAddonInfo('name')
#dbg = ptv.getSetting('default_debug') in ('true')
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, mrknow_Parser, xbmcfilmapi, mrknow_urlparser, mrknow_Player
import json

log = pLog.pLog()


mainUrl = 'http://xbmcfilm.com/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {}


class xbmcfilm:
    def __init__(self):
        log.info('Starting xbmcfilm.pl')
        self.p = mrknow_Player.mrknow_Player()
        self.parser = mrknow_Parser.mrknow_Parser()
        self.up = mrknow_urlparser.mrknow_urlparser()
        #self.settings = settings.TVSettings()
        self.api = xbmcfilmapi.XbmcFilmAPI()


    def listsMainMenu(self, table):
        data = {'id': '0'}
        marek = json.dumps(self.api.getcatalogs(data))
        objs = json.loads(marek)
        for o in objs["data"][0]["children"]: 
            print ("o",o, len(o["children"]))
            if (len(o["children"]) > 0):
                self.add('cdapl', 'main-menu', '[COLOR white]'+ o['title'] + '[/COLOR]', 'None', 'None', 'None', 'None', 'None', True, False,str(o['id']))
            else:
                self.add('cdapl', 'main-menu', '[COLOR white]'+ o['title'] + '[/COLOR]', 'None', 'None', 'None', 'None', 'None', True, False,str(o['id']))
        files = json.dumps(self.api.getfiles(data))
        filesobj = json.loads(files)
        print ("Marel",files)
        print ("objs", filesobj["data"])
        for i in filesobj["data"]:
            self.add('cdapl', 'playSelectedMovie','None',i['title'] , 'None', i['url'], 'None', 'None', False, False,'None')

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def listsItems(self, id):
        data = {'id': id}
        marek = json.dumps(self.api.getcatalogs(data))
        objs = json.loads(marek)
        for o in objs["data"]: 
            print ("o",o, len(o["children"]))
            if (len(o["children"]) > 0):
                self.add('cdapl', 'main-menu', '[COLOR white]'+ o['title'] + '[/COLOR]', 'None', 'None', 'None', 'None', 'None', True, False,str(o['id']))
            else:
                self.add('cdapl', 'main-menu','[COLOR white]'+  o['title'] + '[/COLOR]', 'None', 'None', 'None', 'None', 'None', True, False,str(o['id']))

        files = json.dumps(self.api.getfiles(data))
        filesobj = json.loads(files)
        print ("Marel",files)
        print ("objs", filesobj["data"])
        for i in filesobj["data"]:
            self.add('cdapl', 'playSelectedMovie','None',i['title'], 'None', i['url'], 'None', 'None', False, False,'None')

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
       
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,myid = "0"):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage) + "&myid="+myid
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
            

    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        myid = self.parser.getParam(params, "myid")
        print(name,category,url,title)
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu':
            self.listsItems(myid)
        

        if name == 'playSelectedMovie':
            #self.LOAD_AND_PLAY_VIDEO(url, title, icon)
            data = self.up.getVideoLink(url)
            print ("A1111",data)
            print ("is String",isinstance(data, basestring))
            if isinstance(data, basestring):
                self.p.LOAD_AND_PLAY_VIDEO(data, title, icon, '','','')        			
            else:
                self.p.LOAD_AND_PLAY_VIDEO(data[0], title, icon, '','',data[1])        
  
init = xbmcfilm()
init.handleService()