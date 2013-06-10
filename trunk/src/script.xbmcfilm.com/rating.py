# -*- coding: utf-8 -*-
"""Module used to launch rating dialogues and send ratings to trakt"""

import xbmc
import xbmcaddon
import xbmcgui
import utilities
import globals
from utilities import Debug, xbmcJsonRequest, notification, get_float_setting, get_bool_setting
from xbmcfilmapi import xbmcfilmAPI

__settings__ = xbmcaddon.Addon("script.xbmcfilm.com")
__language__ = __settings__.getLocalizedString

buttons = {
    10030:    'love',
    10031:    'hate',
    11030:    '1',
    11031:    '2',
    11032:    '3',
    11033:    '4',
    11034:    '5',
    11035:    '6',
    11036:    '7',
    11037:    '8',
    11038:    '9',
    11039:    '10'
}

focus_labels = {
    10030: __language__(1314).encode('utf-8', 'ignore'),
    10031: __language__(1315).encode('utf-8', 'ignore'),
    11030: __language__(1315).encode('utf-8', 'ignore'),
    11031: __language__(1316).encode('utf-8', 'ignore'),
    11032: __language__(1317).encode('utf-8', 'ignore'),
    11033: __language__(1318).encode('utf-8', 'ignore'),
    11034: __language__(1319).encode('utf-8', 'ignore'),
    11035: __language__(1320).encode('utf-8', 'ignore'),
    11036: __language__(1321).encode('utf-8', 'ignore'),
    11037: __language__(1322).encode('utf-8', 'ignore'),
    11038: __language__(1323).encode('utf-8', 'ignore'),
    11039: __language__(1314).encode('utf-8', 'ignore')
}


def ratingCheck(current_video, watched_time, total_time, playlist_length,sessionid):
    """Check if a video should be rated and if so launches the rating dialog"""
    #current_video['id'] = 123
    print ("WWWWWWWWW",current_video)
    Debug("[Rating] Rating Check called for '%s' with sessionid=%s" % (current_video['type'], str(sessionid)));
    if get_bool_setting("rate_%s" % current_video['type']):
        watched = (watched_time / total_time) * 100
        if watched >= get_float_setting("rate_min_view_time"):
            if (playlist_length <= 1) or get_bool_setting("rate_each_playlist_item"):
                rateMedia(current_video, current_video['type'],sessionid)
            else:
                Debug("[Rating] Rate each playlist item is disabled.")
        else:
            Debug("[Rating] '%s' does not meet minimum view time for rating (watched: %0.2f%%, minimum: %0.2f%%)" % (current_video['type'], watched, get_float_setting("rate_min_view_time")))
    else:
        Debug("[Rating] '%s' is configured to not be rated." % current_video['type'])


def rateMedia(current_video, media_type,sessionid):
    """Launches the rating dialog"""
    #if media_id == None:
    #    Debug('[Rating] Missing media_id')
    #    return
    #comm='''

#    if not globals.xbmcfilmapi.settings:
#        globals.xbmcfilmapi.getAccountSettings()
    #rating_type = globals.xbmcfilmapi.settings['viewing']['ratings']['mode']
    xbmc.executebuiltin('Dialog.Close(all, true)')

    gui = RatingDialog(
        "RatingDialog.xml",
        __settings__.getAddonInfo('path'),
        media_type=media_type,
        #media_type='movie',
        #media=xbmc_media,
        media={'title': current_video['title'],'year': current_video['year']},
        #rating_type=rating_type
        rating_type='advanced'
        )

    gui.doModal()
    if gui.rating:
        rateOnTrakt(gui.rating, gui.media_type, gui.media,sessionid)
    del gui


def rateOnTrakt(rating, media_type, media,sessionid):
    Debug('[rating] Sending rating (%s) to trakt' % rating)
    if media_type == 'movie':
        params = {'title': media['title'], 'year': media['year'], 'rating': rating, 'id_session':sessionid}

        #if media['imdbnumber'].startswith('tt'):
        #    params['imdb_id'] = media['imdbnumber']

        #elif media['imdbnumber'].isdigit():
        #    params['tmdb_id'] = media['imdbnumber']

        data = globals.xbmcfilmapi.rateMovie(params)

    else:
        params = {'title': media['label'], 'year': media['year'], 'season': media['episode']['season'], 'episode': media['episode']['episode'], 'rating': rating}

        #if media['imdbnumber'].isdigit():
        #    params['tvdb_id'] = media['imdbnumber']

        #elif media['imdbnumber'].startswith('tt'):
        #    params['imdb_id'] = media['imdbnumber']

        data = globals.xbmcfilmapi.rateEpisode(params)
        #data = ''

    if data != None:
        notification(__language__(1201).encode('utf-8', 'ignore'), __language__(1167).encode('utf-8', 'ignore')) # Rating submitted successfully


class RatingDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, xmlFile, resourcePath, defaultName='Default', forceFallback=False, media_type=None, media=None, rating_type=None):
        self.media_type = media_type
        self.media = media
        self.rating_type = rating_type
        self.rating = None

    def onInit(self):
        self.getControl(10014).setVisible(self.rating_type == 'simple')
        self.getControl(10015).setVisible(self.rating_type == 'advanced')

        if self.media_type == 'movie':
            self.getControl(10012).setLabel('%s (%s)' % (self.media['title'], self.media['year']))
        else:
            self.getControl(10012).setLabel('%s - %s' % (self.media['label'], self.media['episode']['label']))

        if self.rating_type == 'simple':
            self.setFocus(self.getControl(10030)) #Focus Loved Button
        else:
            self.setFocus(self.getControl(11037)) #Focus 8 Button


    def onClick(self, controlID):
        if controlID in buttons:
            self.rating = buttons[controlID]
            self.close()


    def onFocus(self, controlID):
        if controlID in focus_labels:
            self.getControl(10013).setLabel(focus_labels[controlID])
        else:
            self.getControl(10013).setLabel('')
