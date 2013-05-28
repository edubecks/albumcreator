# coding: utf-8
from datetime import datetime

__author__ = 'edubecks'

from models import AlbumModel, PictureModel, UserModel
from album import Album

MAX_PICTURES = 12
NEW_ALBUM_FULL = 1


class PersistenceController(object):
    def __init__(self):
        super(PersistenceController, self).__init__()

    def _create_new_album(self, user):
        album = AlbumModel(user=user)
        album.save()
        return album

    def _save_picture(self, picture, album):
        pic = PictureModel(
            url=picture['url'],
            description=picture['description'][:500],
            album=album
        )
        pic.save()
        return

    def get_pictures_by_user(self, user):
        # user = User.objects.get(fb_id=user_id)
        albums = AlbumModel.objects.filter(user=user)
        albums_list = []
        # print 'images in total', PictureModel.objects.count()
        for album in albums:
            pictures = PictureModel.objects.filter(album=album)
            print pictures
            # print len(pictures)
            albums_list.append(
                Album(description=album.description, pictures = pictures).dict_representation()
            )
            # for picture in pictures:
            #     picture_list.append(picture)
        return albums_list

    def new_user(self, fb_id, email=u'test@example.com'):

        ## creating new user
        user = UserModel(fb_id=fb_id, email=email)
        user.save()

        ## creating new album
        self._create_new_album(user)

        return user



    def add_pictures(self, user, pictures):

        ## last modified album
        last_album = AlbumModel.objects.filter(user=user).order_by('modified')[0]

        num_current_pictures = PictureModel.objects.filter(album=last_album).count()
        num_remaining_pictures = MAX_PICTURES - num_current_pictures

        current_album_pictures = pictures[:num_remaining_pictures]
        # print('adding to album', last_album.id)
        for picture in current_album_pictures:
            # print('adding',picture)
            self._save_picture(picture, last_album)

        ## updating album date
        last_album.modified = datetime.utcnow()
        last_album.save()

        ## extra pictures with new album
        if num_remaining_pictures < len(pictures):
            new_album_pictures = pictures[num_remaining_pictures:]

            new_album = self._create_new_album(user)

            for picture in new_album_pictures:
                self._save_picture(picture, new_album)

            ## flag for new album
            return NEW_ALBUM_FULL

        return


    def get_user(self, fb_id):
        user = UserModel.objects.get(fb_id=fb_id)
        return user
