# Create your views here.
import json
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from albumcreator.appcontroller import AppController
from albumcreator.auth import Auth
from albumcreator.models import UserModel
from albumcreator.persistence_controller import PersistenceController
from albumcreator.scrapper import Scrapper


def _pictures_by_user(fb_id):
    return AppController.pictures_for_userid(fb_id)



def _pictures_by_user_json(request, fb_id):
    albums_list = _pictures_by_user(fb_id)
    return HttpResponse(json.dumps(albums_list), content_type="application/json")

def _pictures_by_user_html(request, fb_id):
    albums_list = _pictures_by_user(fb_id)
    data = RequestContext(request, {
        'albums_list': albums_list,
    })
    return render_to_response('index.html', data)

def populate():
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


def pictures(request):
    if (
        'type' in request.GET
        and request.GET['type']
        and 'id' in request.GET
        and request.GET['id']
    ):
        type = request.GET.get('type')
        fb_id = request.GET.get('id')

        type_response = {
            'json': _pictures_by_user_json,
            'html': _pictures_by_user_html
        }
        # populate()
        return type_response[type](request, fb_id)


