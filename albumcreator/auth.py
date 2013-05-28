# coding: utf-8
__author__ = 'edubecks'

import facebook
from pprint import pprint
from config import OAUTH_TOKEN
from facepy.utils import get_extended_access_token


class Auth(object):
    def __init__(self, id):
        super(Auth, self).__init__()

        self._graph = facebook.GraphAPI(OAUTH_TOKEN)
        self._user = id

    def get_albums(self):
        return self._graph.get_connections(self._user, 'albums')

    def get_pictures_from_album(self, album):
        return self._graph.get_connections(album, 'photos')



