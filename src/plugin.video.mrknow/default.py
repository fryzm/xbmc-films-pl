# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon


scriptID = 'plugin.video.mrknow'
scriptname = "Films online"
ptv = xbmcaddon.Addon(scriptID)
print("scripid",ptv)




MENU_TABLE = { #1000: "www.mrknow.pl [filmy online]",
               
               2100: "filmbox.pl",

             #  4200: "livelooker.com",


               9000: "noobroom.com"
}
TV_ONLINE_TABLE = {
		#     2100 : ["Film Box", 'filmbox'],
        #     2200 : ["Plejer.tv", 'plej'],
         #    2300 : ["Team-cast.pl [dziala jak weeb.tv ale za darmo]", 'teamcastpl'],
              2350 : ["Looknij.tv [troche przycina]", 'looknijtv'],
             2400 : ["TVP Stream", 'tvpstream'],
        #     2500 : ["Netvi.tv", 'netvi'],
             2600 : ["Radio81.pl [test 10% dziala, w tym hbo]", 'radio81'],
         #    2700 : ["Streamon.pl", 'streamon'],
             2800 : ["MmTV.pl","mmtv"]
}
FUN_ONLINE_TABLE = {
               3000: ["Wykop.pl","wykop"],
               #6000: ["Milanos.pl","milanos"],
               #4500: ["Tosiewytnie.pl","tosiewytnie"],
               #5000: ["Joemonster.org","joemonster"],
               5100: ["Wrzuta.pl","wrzuta"],
               #5200: ["interia.tv [testy]","interia"]
               
               
}
SPORT_ONLINE_TABLE = {
               4000: ["Meczyki.pl [dziala ok 40%]","meczyki"],
               #4100: ["Drhtv.com.pl","drhtvcompl"],
               #2600 : ["Goodcast.tv", 'goodcast'],
               #2700 : ["Streamon.pl", 'streamon'],
               
}

SERIALE_ONLINE_TABLE = {
               8000: ["Alekino.tv","kinoliveseriale"],
               8100: ["Scs.pl","scs"]
}

FILM_ONLINE_TABLE = {
		     7400 : ["Cda.pl", 'cdapl'],
             7300: ["Polvod.pl","polvod"],
             #7300: ["Noobroom.com","noobroom"],
             7000: ["Vod Onet PL","vodpl"],
             7100: ["Filmbox Movie","filmboxmoovie"],
             7200: ["Seansik.tv","seansiktv"],
             7500: ["Alekino.tv","kinolive"],
             7600: ["Iptak","iptak"],
             #7700: ["Films-online.pl","filmsonline"],
             7800: ["StrefaVod.pl","strefavod"],
             5100: ["Wrzuta.pl [testy]","wrzuta"],
             7900: ["Vod.tvpl.pl [testy]","tvppl"],
             

}
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import wykop, joemonster, milanos,filmbox,vodpl
import kinolive,tvpstream,kinoliveseriale,scs,filmsonline,mmtv, polvod, looknijtv
import iptak,radio81,strefavod,wrzuta,tvppl, interia
import filmboxmoovie, cdapl, seansiktv

class MrknowFilms:
    def __init__(self):
        #BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
        BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
        sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
        sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )
        import mrknow_pLog, settings, Parser

        self.log = mrknow_pLog.pLog()
        self.log.info('Filmy online www.mrknow.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()

    def showListOptions(self):
        params = self.parser.getParams()
        mode = self.parser.getIntParam(params, "mode")
        name = self.parser.getParam(params, "name")
        service = self.parser.getParam(params, 'service')
        if mode == None and name == None and service == None:
            self.log.info('Wyświetlam kategorie')
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
        elif mode == 3:
            self.LIST(SERIALE_ONLINE_TABLE)

        elif mode == 8000 or service == 'kinoliveseriale':
            tv = kinoliveseriale.kinoliveseriale()
            tv.handleService()
        elif mode == 8100 or service == 'scs':
            tv = scs.scs()
            tv.handleService()
        elif mode == 7000 or service == 'vodpl':
            tv = vodpl.vodpl()
            tv.handleService()
        elif mode == 7100 or service == 'filmboxmoovie':
            tv = filmboxmoovie.filmboxmoovie()
            tv.handleService()
        elif mode == 7200 or service == 'seansiktv':
            tv = seansiktv.seansiktv()
            tv.handleService()
        elif mode == 7300 or service == 'polvod':
            tv = polvod.polvod()
            tv.handleService()
        elif mode == 7400 or service == 'cdapl':
            tv = cdapl.cdapl()
            tv.handleService()
        elif mode == 7500 or service == 'kinolive':
            print("KKKKKKKKKKKKKKKKKKKK", sys.argv[1], sys.argv[2], sys.argv[0] )
            tv = kinolive.kinolive()
            tv.handleService()
        elif mode == 7600 or service == 'iptak':
            tv = iptak.IPTAK()
            tv.handleService()
        elif mode == 7700 or service == 'filmsonline':
            tv = filmsonline.filmsonline()
            tv.handleService()
        elif mode == 7800 or service == 'strefavod':
            tv = strefavod.strefavod()
            tv.handleService()
        elif mode == 7900 or service == 'tvppl':
            tv = tvppl.tvppl()
            tv.handleService()

        elif mode == 2100 or service == 'filmbox':
            tv = filmbox.filmbox()
            tv.handleService()
        elif mode == 2350 or service == 'looknijtv':
            tv = looknijtv.looknijtv()
            tv.handleService()
        elif mode == 2400 or service == 'tvpstream':
            tv = tvpstream.tvpstream()
            tv.handleService()
        elif mode == 2600 or service == 'radio81':
            tv = radio81.radio81()
            tv.handleService()
        elif mode == 2800 or service == 'mmtv':
            tv = mmtv.mmtv()
            tv.handleService()
        elif mode == 3000 or service == 'wykop':
            tv = wykop.WYKOP()
            tv.handleService()
        elif mode == 5000 or service == 'joemonster':
            tv = joemonster.joemonster()
            tv.handleService()
        elif mode == 5100 or service == 'wrzuta':
            tv = wrzuta.wrzuta()
            tv.handleService()
        elif mode == 5200 or service == 'interia':
            tv = interia.interia()
            tv.handleService()
        elif mode == 6000 or service == 'milanos':
            tv = milanos.milanos()
            tv.handleService()
        elif mode == 7200 or service == 'seansiktv':
            tv = seansiktv.seansiktv()
            tv.handleService()


        elif mode == 20:
            self.log.info('Wyświetlam ustawienia')
            self.settings.showSettings()

    def CATEGORIES(self):
        self.addDir("Telewizja", 1, False, 'Telewizja', False)
        self.addDir("Filmy", 2, False, 'Filmy', False)
        self.addDir("Seriale", 3, False, 'Seriale', False)
        self.addDir("Rozrywka", 4, False, 'Rozrywka', False)
        #self.addDir('Sport', 19, False, 'Sport', False)
        self.addDir('Ustawienia', 20, True, 'Ustawienia', False)
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
        #print("Dane",name, mode, autoplay, icon, isPlayable)
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
