# -*- coding: utf-8 -*-
# RP-Podcasts: a fan-made Kodi add-on for the podcasts of the "Rheinische Post" newspaper
# Source code and bug reports: https://github.com/zimbelstern/kodi-addon-rp-podcasts
# Copyright (c) 2018 Walfried Schneider
# Published under the MIT License.

import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import podparser
import urllib
import urlparse

addon_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
resources_path = os.path.join(addon_path, 'resources')
images_path = os.path.join(resources_path, 'images')

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'audio')

mode = args.get('mode')
foldername = args.get('foldername')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def createListItem(episodelist, whichone):
    data = episodelist.getListItem(whichone)
    li = xbmcgui.ListItem(data[1])
    li.setArt({"thumb":data[2]})
    li.setInfo("music", {"title":data[3]})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=data[0], listitem=li)

episodeinfo = {}
for podcast in ['aufwacher', 'rheinpegel', 'praktischfaktisch']:
    episodeinfo[podcast] = podparser.EpisodeList(podcast, images_path)
    episodeinfo[podcast].readFeed()

if mode == None:

    for podcast in ['aufwacher', 'rheinpegel', 'praktischfaktisch']:
        createListItem(episodeinfo[podcast], 0)

    url = build_url({'mode': 'folder', 'foldername': 'aufwacher'})
    li = xbmcgui.ListItem('Ältere Folgen Aufwacher', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'rheinpegel'})
    li = xbmcgui.ListItem('Ältere Folgen Rheinpegel', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'praktischfaktisch'})
    li = xbmcgui.ListItem('Ältere Folgen Praktisch Faktisch', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    for i in range(len(episodeinfo[foldername[0]].episodelist)-1):
        createListItem(episodeinfo[foldername[0]], i+1)
    xbmcplugin.endOfDirectory(addon_handle)

