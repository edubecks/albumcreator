# coding: utf-8
from pprint import pprint

__author__ = 'edubecks'


class Scrapper(object):
    def __init__(self, auth):
        super(Scrapper, self).__init__()
        self.auth = auth

    def scrap(self):
        albums = self.auth.get_albums()
        num_albums = albums['data']['']
        return

    def scrap_album(self, album_num=1, num_pictures=3):
        albums = self.auth.get_albums()
        ## selecting album
        fb_album = albums['data'][album_num]
        # pprint(fb_album)
        fb_album_id = fb_album['id']
        fb_album_num_pictures = fb_album['count']

        fb_pictures = self.auth.get_pictures_from_album(fb_album_id)['data']
        # pprint(fb_pictures[0])

        pictures = []
        for i in xrange(min(fb_album_num_pictures, num_pictures)):
            pic = {
                'url': fb_pictures[i]['source'],
                'id': fb_pictures[i]['id'],
                'description': fb_pictures[i]['name'] if 'name' in fb_pictures[i] else 'Untitled',

            }
            # pprint(pic)
            pictures.append(pic)

        return pictures
