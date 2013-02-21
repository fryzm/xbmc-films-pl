# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon

scriptID = 'plugin.image.mrknow'
scriptname = "Images online"
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, Parser
 
import demotywatory


log = pLog.pLog()


MENU_TABLE = { #1000: "www.mrknow.pl ",
               2000: "demotywatory.pl"
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
        #self.CATEGORIES()
        self.LIST(MENU_TABLE)
    elif mode == 2000 or service == 'demotywatory':
        tv = demotywatory.demotywatory()
        tv.handleService()
    


  def listsTable(self, table):
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def LIST(self, table = {}):
   for num, val in table.items():
    self.addDir(val, num, False, False)
   xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def addDir(self, name, mode, autoplay, isPlayable = True):
    u=sys.argv[0] + "?mode=" + str(mode)
    icon = "DefaultVideoPlaylists.png"
    if autoplay:
      icon= "DefaultVideo.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Image", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)

init = MrknowFilms()
init.showListOptions()
