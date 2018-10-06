# -*- coding: utf-8 -*-
# RP Podcasts: a fan-made Kodi add-on for the podcasts of the "Rheinische Post" newspaper
# Source code and bug reports: https://github.com/zimbelstern/rp-podcasts
# Copyright (c) 2018 Walfried Schneider
# Published under the MIT License.

import os
import xml.etree.ElementTree as et
import urllib
import urllib2
import time
from datetime import datetime

# Dictionaries
feedname_to_url = {'aufwacher' : 'https://podcasts.rp-online.de/aufwacher/feed/podcast/', 'rheinpegel' : 'https://podcasts.rp-online.de/rheinpegel/feed/podcast/', 'praktischfaktisch' : 'https://podcasts.rp-online.de/gutleben/feed/podcast/'}

feedname_to_feedtitle = {'aufwacher' : 'Aufwacher', 'rheinpegel' : 'Rheinpegel', 'praktischfaktisch' : 'Praktisch Faktisch'}

german_dow = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag']

class EpisodeList:
    """Contains information on the feed and the episodes retrieved by HTTP. Needs a path to thumbnail images."""
    def __init__(self, feedname, image_dir):
        """Initialises variables. Needs feedname and image directory."""
        self.feedname = feedname
        self.feedurl = feedname_to_url[self.feedname]
        self.feedtitle = feedname_to_feedtitle[self.feedname]
        self.episodelist = []
        self.image_dir = image_dir
        self.feedimage = os.path.join(self.image_dir, self.feedname + '.jpg')

    def readFeed(self):
        """Reads the feed and creates list of episodes."""
        try:
            self.tree = et.parse(urllib2.urlopen(self.feedurl))
            self.root = self.tree.getroot()
#            self.feedtitle = self.root.find('channel').find('title').text # alternative title
        except:
            return "Error while fetching information from the web. No internet connection?"

        if not os.path.isfile(self.feedimage):
            try:
                urllib.urlretrieve(self.root.find('channel').find('image').find('url').text, self.feedimage)
            except:
                return "Error while downloading thumbnail image."

        try:
            for item in self.root.find('channel').findall('item'):
                title = item.find('title').text
                date = datetime(*(time.strptime(item.find('pubDate').text[:16], '%a, %d %b %Y')[0:6])) # Bugfix as discussed on https://forum.kodi.tv/showthread.php?pid=2416605
                description = item.find('description').text
                url = item.find('enclosure').attrib['url']
                self.episodelist.append({'title' : title, 'date' : date, 'description' : description, 'url' : url, })
            return True
        except:
            return "Error while parsing feed information. Bad feed format?"

    def getListItem(self, entry_item):
        """Returns the audio file url, a parsed title, the thumbnail path and description of an episode list entry."""
        pubdate = self.episodelist[entry_item]['date']
        parsed_pubdate = german_dow[int(datetime.strftime(pubdate, '%w'))] + datetime.strftime(pubdate, ', %d.%m.%Y')
        title = self.feedtitle + " von " + parsed_pubdate
        icon = self.feedimage
        url = self.episodelist[entry_item]['url']
        description = self.episodelist[entry_item]['description']
        return [url, title, icon, description]

if __name__ == '__main__':

    print "This is the python library >podparser< for the kodi plugin >plugin.audio.rp-podcasts<, not for standalone use."
