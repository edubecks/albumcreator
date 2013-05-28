# coding: utf-8
__author__ = 'edubecks'

from unidecode import unidecode


class Album(object):

    def __init__(self, description, pictures):
        super(Album, self).__init__()
        self.description = description
        self.pictures = pictures

    def __len__(self):
        return len(self.pictures)

    def __str__(self):
        return str(self.pictures)

    def dict_representation(self):
        pictures = []
        for pic in self.pictures:
            print pic.url
            pictures.append({
                'description': unidecode(pic.description),
                'url': unidecode(pic.url)
            })

        album_repr = {
            'description':self.description,
            'pictures': pictures
        }
        return album_repr
