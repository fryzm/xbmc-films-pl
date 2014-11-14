# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math, time
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,urlparse
import json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - cda.pl"
ptv = xbmcaddon.Addon(scriptID)
datapath = xbmc.translatePath(ptv.getAddonInfo('profile'))

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import mrknow_pLog, mrknow_pCommon, mrknow_Parser, mrknow_urlparser, mrknow_Pageparser

log = mrknow_pLog.pLog()

mainUrl = 'http://team-cast.pl.cp-21.webhostbox.net/'

MENU_TAB = {1: "Kanały",
            #8: "Video najlepiej ocenione",
            #9: "Krótkie filmy i animacje",
            #10: "Filmy Extremalne",
            #11: "Motoryzacja, wypadki",
            #12: "Muzyka",
            #13: "Prosto z Polski",
            #14: "Rozrywka",
            #15: "Różności",
            #16: "Sport",
            #17: "Śmieszne filmy",
            27: "[COLOR yellow]Aktualizuj LIBRTMP - aby dzialy kanaly TV - Patche KSV[/COLOR]"            }

max_stron = 0            

class StopDownloading(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class teamcastpl:
    def __init__(self):
        log.info('Starting teamcastpl.pl')
        self.cm = mrknow_pCommon.common()
        self.parser = mrknow_Parser.mrknow_Parser()
        self.pp = mrknow_Pageparser.mrknow_Pageparser()
        self.up = mrknow_urlparser.mrknow_urlparser()

        
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('teamcastpl', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsCategoriesMenu(self,url):
        query_data = { 'url': url, 'use_host': True, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<ul class="greybox">(.*?)</ul>', re.DOTALL).findall(link)
        print("Match-->",match)
        valTab = []
        strTab = []
        if len(match)>0:
            for l in range(len(match)):
                print("Match->L>",match[l])
                match1 = re.compile('<li><a href="(.*?)">(.*?)<img src="http://wrzucaj.net/images/2014/09/12/flash-player-icon.png" /></a></li>\n').findall(match[l])
                if len(match1)>0:
                    for j in range(len(match1)):
                        #print("MAtch1",match1[j])
                        strTab.append(mainUrl+ match1[j][0])
                        strTab.append(match1[j][1])
                        valTab.append(strTab)
                        strTab = []
                valTab.sort(key = lambda x: x[1])
            for i in valTab:
                self.add('teamcastpl', 'playSelectedMovie', 'None', i[1], 'None', i[0], 'None', 'None', False, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = 'http://www.cda.pl/video/show/' + urllib.quote_plus(key) +'/p1?s=best'
        #http://www.cda.pl/video/show/xxx/p2?s=best
        return url

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
            xbmcPlayer.play(videoUrl, liz)
            
            if not xbmc.Player().isPlaying():
                xbmc.sleep( 10000 )
                #xbmcPlayer.play(url, liz)
            
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu.', 'Problem')        
        return ok

    def LIBRTMP(self):
        #url='http://www.mediafire.com/api/folder/get_content.php?folder_key='+murl+'&chunk=1&content_type=folders&response_format=json&rand=1789'
        url = 'http://xbmcfilm.com/static/librtmp/librtmp.json'
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        objs = json.loads(link)
        for o in objs:
            self.add('teamcastpl','librtmp','update',o,'None',objs[o],'None','None',True,False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def _pbhook(self,numblocks, blocksize, filesize, dp, start_time):
            try:
                percent = min(numblocks * blocksize * 100 / filesize, 100)
                currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
                kbps_speed = numblocks * blocksize / (time.time() - start_time)
                if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed
                else: eta = 0
                kbps_speed = kbps_speed / 1024
                total = float(filesize) / (1024 * 1024)
                mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total)
                e = 'Speed: %.02f Kb/s ' % kbps_speed
                e += 'ETA: %02d:%02d' % divmod(eta, 60)
                dp.update(percent, mbs, e)
            except:
                percent = 100
                dp.update(percent)
            if dp.iscanceled():
                dp.close()
                raise StopDownloading('Stopped Downloading')

    def DLLIBRTMP(self,mname,url):
        import os
        dialog = xbmcgui.Dialog()
        if re.search('(?i)windows',mname):
                path=xbmc.translatePath('special://xbmc/system/players/dvdplayer/')
        if re.search('(?i)ios',mname):
            ret = dialog.select('[COLOR=FF67cc33][B]Select Device[/COLOR][/B]',['iDevice','ATV2'])
            if ret == -1:
                return
            elif ret == 0:
                path=xbmc.translatePath('special://xbmc')
                path=path.replace('XBMCData/XBMCHome','Frameworks')
            elif ret == 1:
                path=xbmc.translatePath('special://xbmc')
                path=path.replace('XBMCData/XBMCHome','Frameworks')
        if re.search('(?i)android',mname):
            path=xbmc.translatePath('/data/data/org.xbmc.xbmc/lib/')
        if re.search('(?i)linux',mname):
            if re.search('(?i)32bit',mname):
                retex = dialog.select('[COLOR=FF67cc33][B]Select Device[/COLOR][/B]',['Linux Build','ATV1'])
                if retex == -1:
                    return
                elif retex == 0:
                    path=xbmc.translatePath(datapath)
                elif retex == 1:
                    path=xbmc.translatePath(datapath)
            else:
                path=xbmc.translatePath(datapath)
        if re.search('(?i)mac',mname):
            path=xbmc.translatePath('special://xbmc')
            path=path.replace('Resources/XBMC','Frameworks')
        if re.search('(?i)raspi',mname):
            path=xbmc.translatePath('/opt/xbmc-bcm/xbmc-bin/lib/xbmc/system/')

        if re.search('APKINSTALLER',mname):
            path=xbmc.translatePath('special://home')
        name = url.split('/')[-1]
        lib=os.path.join(path,name)
        self.downloadFileWithDialog(url,lib)
        if re.search('(?i)linux',mname):
            keyb = xbmc.Keyboard('', 'Enter Root Password')
            keyb.doModal()
            if (keyb.isConfirmed()):
                sudoPassword = keyb.getText()
                if retex == 1:
                    command = 'mv '+lib+' /usr/lib/i386-linux-gnu/'
                else:
                    command = 'mv '+lib+' /usr/lib/'
                p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
                os.remove(lib)
        if re.search('APKINSTALLER',mname):
            dialog.ok("mrknow.pl", "Thats It All Done", "[COLOR blue]Download location[/COLOR]",path)
        else:
            dialog.ok("mrknow.pl", "Thats It All Done", "[COLOR blue]Now should be Updated[/COLOR]")


    def downloadFileWithDialog(self,url,dest):
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("mrknow.pl","Downloading & Copying File",'')
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: self._pbhook(nb,bs,fs,dp,time.time()))
        except Exception, e:
            dialog = xbmcgui.Dialog()
            #main.ErrorReport(e)
            dialog.ok("Mash Up", "Report the error below at ", str(e), "We will try our best to help you")

    def getMovieLinkFromXML(self, url):
        #szukamy iframe
        progress = xbmcgui.DialogProgress()
        progress.create('Postęp', '')
        message = "Szukam adresu do wideo"
        progress.update( 10, "", message, "" )
        xbmc.sleep( 1000 )
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<iframe name="stream"(.*?)src="(.*?)"(.*?)> </iframe>').findall(link)
        print("Match-->",match)
        progress.update( 30, "", message, "" )
        progress.update( 50, "", message, "" )
        VideoLink = ''
        if len(match)>0:
            message = "Mam adres wideo, dekoduję..."
            progress.update( 60, "", message, "" )
            VideoLink = self.pp.getVideoLink(match[0][1])
            progress.update( 90, "", message, "" )
        progress.close()
        return VideoLink

    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        strona = self.parser.getParam(params, "strona")
        print("Dane",sys.argv[2],url,name,category,title)
        print ("A")

        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == "[COLOR yellow]Aktualizuj LIBRTMP - aby dzialy kanaly TV - Patche KSV[/COLOR]":
            self.LIBRTMP()
        elif name == 'librtmp' and category == "update":
            self.DLLIBRTMP(title,url)
        elif name == 'main-menu' and category == 'Kanały':
            self.listsCategoriesMenu(mainUrl)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
