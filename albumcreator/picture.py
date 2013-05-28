# coding: utf-8
__author__ = 'edubecks'

# coding: utf-8
__author__ = 'edubecks'


class Picture(object):
    def __init__(self, picture_model):
        self.description = picture_model.description
        self.url = picture_model.url

    def __str__(self):
        return len(self.pictures)
