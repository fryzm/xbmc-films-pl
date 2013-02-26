# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon

scriptID = 'plugin.video.mrknow'
scriptname = "Films online"
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, Parser
#import iptak, mrknowpl, tosiewytnie, noobroom
import noobroom, iptak, wykop, meczyki, joemonster, tosiewytnie, drhtvcompl, milanos,filmbox
#import weebtv, ipla, stations, tvp, tvn, iplex, tvpvod, iptak

log = pLog.pLog()


MENU_TABLE = { #1000: "www.mrknow.pl [filmy online]",
               
               2100: "filmbox.pl",

             #  4200: "livelooker.com",


               9000: "noobroom.com"
}
TV_ONLINE_TABLE = {
		     2100 : ["Film Box [wyświetl kanały]", 'filmbox']
}
FUN_ONLINE_TABLE = {
               3000: ["wykop.pl","wykop"],
               6000: ["milanos.pl","milanos"],
               4500: ["tosiewytnie.pl","tosiewytnie"],               
               5000: ["joemonster.org","joemonster"]
}
SPORT_ONLINE_TABLE = {
               4000: ["meczyki.pl","meczyki"],
               4100: ["drhtv.com.pl","drhtvcompl"]
}

FILM_ONLINE_TABLE = {
		     #2000 : ["Iptak.pl", 'iptak'],
             #9000: ["noobroom.com","noobroom"]
}

class MrknowFilms:
  def __init__(self):
    log.info('Filmy online www.mrknow.pl')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()

  def showListOptions(self):
    params = self.parser.getParams()
    mode = self.parser.getIntParam(params, "mode")
    name = self.parser.getParam(params, "name")
    service = self.parser.getParam(params, 'service')    
    if mode == None and name == None and service == None:
        log.info('Wyświetlam kategorie')
        self.CATEGORIES()
        #self.LIST(MENU_TABLE)        
    elif mode == 1:
        self.LIST(TV_ONLINE_TABLE)
    elif mode == 4:
        self.LIST(FUN_ONLINE_TABLE)
    elif mode == 19:
        self.LIST(SPORT_ONLINE_TABLE)
    elif mode == 2:
        self.LIST(FILM_ONLINE_TABLE)
        
    elif mode == 1000 or service == 'mrknowpl':
        tv = mrknowpl.mrknowpl()
        tv.handleService()
    elif mode == 2000 or service == 'iptak':
        tv = iptak.IPTAK()
        tv.handleService()
    elif mode == 2100 or service == 'filmbox':
        tv = filmbox.filmbox()
        tv.handleService()
    elif mode == 3000 or service == 'wykop':
        tv = wykop.WYKOP()
        tv.handleService()
    elif mode == 4000 or service == 'meczyki':
        tv = meczyki.MECZYKI()
        tv.handleService()
    elif mode == 4100 or service == 'drhtvcompl':
        tv = drhtvcompl.drhtvcompl()
        tv.handleService()
        
    elif mode == 4200 or service == 'livelooker':
        tv = livelooker.livelooker()
        tv.handleService()
        
    elif mode == 5000 or service == 'joemonster':
        tv = joemonster.joemonster()
        tv.handleService()
    elif mode == 9000 or service == 'noobroom':
        tv = noobroom.Noobroom()
        tv.handleService()
    elif mode == 4500 or service == 'tosiewytnie':
        tv = tosiewytnie.ToSieWytnie()
        tv.handleService()
    elif mode == 6000 or service == 'milanos':
        tv = milanos.milanos()
        tv.handleService()

  def CATEGORIES(self):

        self.addDir("Telewizja", 1, False, 'telewizja', False)
#        self.addDir("Filmy", 2, False, 'film', False)
        self.addDir("Rozrywka", 4, False, 'rozrywka', False)
        self.addDir('Sport', 19, False, 'nagrywanie', False)
#        self.addDir('Ustawienia', 20, True, 'ustawienia', False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

  def listsTable(self, table):
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def LIST(self, table = {}):
      valTab = []
      strTab = []
      for num, tab in table.items():
          strTab.append(num)
          strTab.append(tab[0])
	  strTab.append(tab[1])
          valTab.append(strTab)
          strTab = []
      valTab.sort(key = lambda x: x[1])      
      for i in range(len(valTab)):
          if valTab[i][2] == '': icon = False
          else: icon = valTab[i][2]
          self.addDir(valTab[i][1], valTab[i][0], False, icon, False)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def addDir(self, name, mode, autoplay, icon, isPlayable = True):
    u=sys.argv[0] + "?mode=" + str(mode)
    if icon != False:
      icon = os.path.join(ptv.getAddonInfo('path'), "images/") + icon + '.png'
    else:
      icon = "DefaultVideoPlaylists.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)

init = MrknowFilms()
init.showListOptions()
