# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import urlparse, string


scriptID = 'plugin.video.mrknow'
scriptname = "www.mrknow.pl - demotywatory"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser

log = pLog.pLog()
itemsperpage=10
mainUrl = 'http://demotywatory.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Wszystkie", }
            #3: "Szukaj" }


class demotywatory:
    def __init__(self):
        log.info('Starting demotywatory.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()



    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('demotywatory', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        ile = int(self.getSizeAllItems())/int(itemsperpage)
        print ("Ile", ile)
        for num in range(1, ile):
            self.add('demotywatory', 'categories-menu', 'Strona ' + str(num), 'None', 'None', mainUrl + 'page/' + str(num*itemsperpage), 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def gettitle(self,txt):
        txt =  ' '.join(str(txt).translate(None, string.whitespace[:5]).split())
        txt = txt.replace("&nbsp;", "")
        return txt

    def getpage(self, url):
        query = urlparse.urlparse(url)
        channel = query.path
        params = query.path.split("/")
        ile = int(params[2])
        for c in range((ile-itemsperpage+1),ile):
            req = urllib2.Request(mainUrl+'page/'+ str(c))
            req.add_header('User-Agent', HOST)
            openURL = urllib2.urlopen(req)
            readURL = openURL.read()
            openURL.close()
            match = re.compile('<div class="\r\n\t demot_pic\r\n\t (.*?)\t \t ">(.*?)</div>', re.DOTALL).findall(readURL)
            match = re.compile('<div class="demotivator pic" id="(.*?)">(.*?)</div>', re.DOTALL).findall(readURL)
            #print ("Match",len(match),match)
            if len(match) > 0:
                for i in range(len(match)):
                    if str(match[i]).find('video') > -1:
                        log.info("Video, ignoruję ....")
                       # match1 = re.compile('<img src="(.*?)"(.*?)/>',re.DOTALL).findall(match[i][1])
                       # match2 = re.compile('<h2 style="display:none;" >(.*?)</h2>',re.DOTALL).findall(match[i][1])
                       # match3 = re.compile('<iframe(.*?)src="(.*?)"(.*?)</iframe>',re.DOTALL).findall(match[i][1])
                       # linkVideo = self.up.getVideoLink(match3[0][1])
                       # self.add('demotywatory', 'playSelectedMovie', 'None', self.gettitle(match2[0]), match1[0][0], linkVideo, 'aaaa', 'Video', False, True,i)
                        
                    else:
                        match1 = re.compile('<img src="(.*?)"(.*?)/>',re.DOTALL).findall(match[i][1])
                        match2 = re.compile('<h2(.*?)>(.*?)</h2>',re.DOTALL).findall(match[i][1])
                        if len(match1)>0 and  len(match2)>0:
                            self.add('demotywatory', 'playSelectedMovie', 'None', self.gettitle(match2[0][1]), match1[0][0], match1[0][0], 'aaaa', 'Image', False, True,100)
        

    def listsItems(self, url):
        # for num in range(1,10):
        self.getpage(url)
        xbmcplugin.endOfDirectory(handle=(int(sys.argv[1])), succeeded=True, updateListing=False, cacheToDisc=True)
   

    def getSizeAllItems(self):
        numItems = 0
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<div class="paginator" id="paginator_3000"></div>(.*?)</script>', re.DOTALL).findall(readURL)
        match1 = re.compile('"paginator_3000",                  					(.*?), 					20,', re.DOTALL).findall(match[0])
        return match1[0]
    
    

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    
    def add(self, service, name, category, title, iconimage, url, desc, type='Image', folder = True, isPlayable = True, total=0):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
            liz.setInfo( type=type, infoLabels={ "Title": title } )
            #liz.setInfo( infoLabels={ "Title": title } )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=folder, totalItems=total)
        else:
            liz.setInfo( type="Video", infoLabels={ "Title": title } )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
 
           
    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Wszystkie':
            log.info('Jest Wszystkie: ')
            self.listsCategoriesMenu()
            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)


        
  
