import simplejson
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_simple_response.http import to_http, JSONResponse, FileResponse, is_serializable
from django_simple_response.consts import DEFAULT_STATUS_CODE


class SimpleResponseTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get_or_create(username='username')[0]

    def assertResponse(self, value, type_of_response, type_of_content):
        request = self.factory.get('/')
        response = to_http( request, value )
        self.assertEqual( response.status_code, DEFAULT_STATUS_CODE )
        self.assertTrue( isinstance(response, type_of_response) )       
        try:
            content = simplejson.loads(response.content)
        except simplejson.scanner.JSONDecodeError:
            content = response.content
        self.assertEqual( type(content), type_of_content ) 
    
    def test_home_view(self):
        response = Client().get("/")
        self.assertEqual( response.status_code, 401 )
        self.assertEqual( response.content, "Not authorized" )
        
    def test_to_http(self):
        self.assertResponse(HttpResponse(), 
            type_of_response = HttpResponse, 
            type_of_content  = str) 
        self.assertResponse(None, 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse(True, 
            type_of_response = JSONResponse,
            type_of_content  = bool)
        self.assertResponse(1.0, 
            type_of_response = HttpResponse,
            type_of_content  = float)
        self.assertResponse("", 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse(DEFAULT_STATUS_CODE, 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse({}, 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse([], 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(User.objects.values(), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(User.objects.all(), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(self.user, 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse((i for i in range(9)), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(open(__file__), 
            type_of_response = FileResponse,
            type_of_content  = str)
        self.assertResponse(iter(range(9)), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(type('X', (object,),{}), 
            type_of_response = HttpResponse,
            type_of_content  = str)
