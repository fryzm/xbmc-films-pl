# -*- coding: utf-8 -*-
import re, sys, os, cgi
import urllib, urllib2
import xbmcgui,xbmc, mrknow_pCommon, xbmcaddon, time

ptv = xbmcaddon.Addon()
scriptID = ptv.getAddonInfo('id')
scriptname = ptv.getAddonInfo('name')
#dbg = ptv.getSetting('default_debug') in ('true')
ptv = xbmcaddon.Addon(scriptID)

class mrknow_Player:
    def __init__(self):
        self.cm = mrknow_pCommon.common()    

    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon,year='',plot='',subs=''):
        if videoUrl == '':
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu', 'Mo�e to chwilowa awaria.', 'Spr�buj ponownie za jaki� czas')
            return False
        if icon == '' or  icon == 'None':
            icon = "DefaultVideo.png"
        if plot == '' or plot == 'None':
            plot = ''
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        if year == '':
            liz.setInfo( type="video", infoLabels={ "Title": title,"Plot": plot} )
        else:
            liz.setInfo( type="video", infoLabels={ "Title": title, "Plot": plot, "Year": int(year) } )
        
        if subs != '':
            subsdir = os.path.join(ptv.getAddonInfo('path'), "subs")
            if not os.path.isdir(subsdir):
                os.mkdir(subsdir)
            query_data = { 'url': subs, 'use_host': False, 'use_header': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            data = self.cm.getURLRequestData(query_data)
            output = open((os.path.join(subsdir, "napisy.txt" )),"w+")
            output.write(data)
            output.close()
            time.sleep(6)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)
            #xbmcPlayer.Player().setSubtitles((os.path.join(subsdir, "napisy.txt" )))
            #xbmcPlayer.Player().showSubtitles(True)
            for _ in xrange(30):
                if xbmcPlayer.isPlaying():
                    break
                time.sleep(1)
            else:
                raise Exception('No video playing. Aborted after 30 seconds.')
            xbmcPlayer.setSubtitles((os.path.join(subsdir, "napisy.txt" )))
            xbmcPlayer.showSubtitles(True)        
        else:
             xbmcPlayer = xbmc.Player()
             xbmcPlayer.play(videoUrl, liz)

        