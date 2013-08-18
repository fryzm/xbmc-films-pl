# -*- coding: utf-8 -*-
import re, sys, os, cgi
import urllib, urllib2
import xbmcgui,xbmc

scriptID = sys.modules[ "__main__" ].scriptID
scriptname = "mrknow Polish films online"

class Player:
    def __init__(self):
        pass
    
    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon,year='',plot=''):
        print ("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",title, icon,year,plot)
        if icon == '' or  icon == 'None':
            icon = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        if year == '':
            liz.setInfo( type="Video", infoLabels={ "Title": title} )
        else:
            liz.setInfo( type="Video", infoLabels={ "Title": title, "Plot": plot, "Year": int(year) } )
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoUrl, liz)
        return True