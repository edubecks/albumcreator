"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from pprint import pprint
from django.http import HttpResponse

from django.test import TestCase, RequestFactory
from albumcreator.auth import Auth
from persistence_controller import PersistenceController
from models import UserModel
from albumcreator.scrapper import Scrapper
from views import pictures


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ScrapperTest(TestCase):
    def test_album(self):
        user_id = '677153213'
        auth = Auth(user_id)

        scrapper = Scrapper(auth)
        scrapper.scrap_album()
        return


class AlbumCreatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AlbumCreatorTest, cls).setUpClass()

        ## me
        fb_id = '677153213'
        persistence_controller = PersistenceController()
        persistence_controller.new_user(fb_id=fb_id)

    def test_create_album(self):
        users = UserModel.objects.all()
        user0 = users[0]

        persistence_controller = PersistenceController()
        new_album = persistence_controller._create_new_album(user=user0)

        self.assertEqual(user0, new_album.user, 'album created OK')
        return

    def test_add_pictures(self):
        users = UserModel.objects.all()
        user0 = users[0]

        auth = Auth(user0.fb_id)
        # return

        scrapper = Scrapper(auth)
        pictures = scrapper.scrap_album()

        persistence_controller = PersistenceController()
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        albums_of_pictures = persistence_controller.get_pictures_by_user(user0)


        def count_total_pictures_in_album(albums_of_pictures):
            num = 0
            for album in albums_of_pictures:
                num += len(album)
            return num

        # pprint(albums_of_pictures)
        # pprint(count_total_pictures_in_album(albums_of_pictures))

        ## 1 album with 3 images
        self.assertEqual(
            1,
            len(albums_of_pictures),
            'Wrong number of albums:' + str(len(pictures)) + ' vs ' + str(len(albums_of_pictures))
        )
        self.assertEqual(len(pictures),
                         count_total_pictures_in_album(albums_of_pictures),
                         'Not all the images were retrieved')


        ## adding more images
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        albums_of_pictures = persistence_controller.get_pictures_by_user(user0)

        ## 1 album with 9 images
        self.assertEqual(
            1,
            len(albums_of_pictures),
            'Wrong number of albums:' + str(len(pictures)) + ' vs ' + str(len(albums_of_pictures))
        )
        self.assertEqual(
            9,
            count_total_pictures_in_album(albums_of_pictures),
            'Not all the images were retrieved:'+' 9 '+ ' vs ' + str(count_total_pictures_in_album(albums_of_pictures))
        )


        ## adding 3 more images
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        albums_of_pictures = persistence_controller.get_pictures_by_user(user0)
        ## 1 album with 12 images
        self.assertEqual(
            1,
            len(albums_of_pictures),
            'Wrong number of albums:' + str(len(pictures)) + ' vs ' + str(len(albums_of_pictures))
        )
        self.assertEqual(12,
                         count_total_pictures_in_album(albums_of_pictures),
                         'Not all the images were retrieved')

        ## adding 3 more images
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        albums_of_pictures = persistence_controller.get_pictures_by_user(user0)
        ## 2 album with 15 images
        self.assertEqual(
            2,
            len(albums_of_pictures),
            'Wrong number of albums:' + str(len(pictures)) + ' vs ' + str(len(albums_of_pictures))
        )
        self.assertEqual(15,
                         count_total_pictures_in_album(albums_of_pictures),
                         'Not all the images were retrieved')

        return


class APITest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


        ## creating user
        fb_id = '677153213'
        persistence_controller = PersistenceController()
        persistence_controller.new_user(fb_id=fb_id)

        users = UserModel.objects.all()
        user0 = users[0]

        auth = Auth(user0.fb_id)
        scrapper = Scrapper(auth)
        pictures = scrapper.scrap_album()

        persistence_controller = PersistenceController()
        persistence_controller.add_pictures(user=user0, pictures=pictures)
        # albums_of_pictures = persistence_controller.get_pictures_by_user(user0)

        # Every test needs access to the request factory.

    def test_json(self):
        url = 'pictures'
        data_headers = {
            'id':'677153213',
            'type':'json'
        }
        request = self.factory.get(url, data=data_headers)
        response = pictures(request)
        pprint(response)
        pprint(response.content)
        json_repr = json.loads(response.content)
        pprint(json_repr)

