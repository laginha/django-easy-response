import simplejson
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from easy_response.http import JSONResponse, FileResponse
from easy_response.utils.process import to_http
from easy_response.utils import is_tuple
from easy_response.consts import BASIC_SERIALIZATION, DEFAULT_STATUS_CODE
from datetime import date


class SimpleResponseTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get_or_create(username='username')[0]

    def to_http(self, content, basic):
        request = self.factory.get('/')
        return to_http( request, content, basic_serialization=basic )

    def assertTypeOfContent(self, response, type_):
        try:
            content = simplejson.loads(response.content)
        except simplejson.scanner.JSONDecodeError:
            content = response.content
        self.assertEqual( type(content), type_ )

    def assertTypeOfResponse(self, response, type_):
        self.assertTrue( isinstance(response, type_) )

    def assertStatusCode(self, response, value):
        if is_tuple(value):
            self.assertEqual( response.status_code, value[0] )
        else:
            self.assertEqual( response.status_code, DEFAULT_STATUS_CODE )

    def assertResponse(self, value, type_of_response, type_of_content, basic_serialization=BASIC_SERIALIZATION):
        response = self.to_http(value, basic_serialization)
        self.assertTypeOfResponse( response, type_of_response ) 
        self.assertStatusCode( response, value )    
        self.assertTypeOfContent( response, type_of_content )
        return response
    
    #
    # TESTS
    #
    
    def test_home_view(self):
        response = Client().get("/")
        self.assertEqual( response.status_code, 401 )
        self.assertEqual( response.content, "Not authorized" )
    
    def test_template(self):
        response = self.assertResponse((400, "home.html"), 
            type_of_response = HttpResponse,
            type_of_content  = str)
        assert response.content == "This is a template"
        self.assertResponse((400, "home.html", {'foo':'bar'}), 
            type_of_response = HttpResponse,
            type_of_content  = str)
        assert response.content == "This is a template"
        self.assertResponse("home.html", 
            type_of_response = HttpResponse,
            type_of_content  = str)
        assert response.content == "This is a template"
    
    def test_none(self):
        self.assertResponse((400, None), 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse(None, 
            type_of_response = HttpResponse,
            type_of_content  = str)
            
    def test_bool(self):
        self.assertResponse((400, True), 
            type_of_response = JSONResponse,
            type_of_content  = bool)
        self.assertResponse(True, 
            type_of_response = JSONResponse,
            type_of_content  = bool)
        
    def test_float(self):
        self.assertResponse((400, 1.0), 
            type_of_response = HttpResponse,
            type_of_content  = float)
        self.assertResponse(1.0, 
            type_of_response = HttpResponse,
            type_of_content  = float)
    
    def test_str(self):
        self.assertResponse((400, ""), 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse("", 
            type_of_response = HttpResponse,
            type_of_content  = str)
    
    def test_int(self):
        self.assertResponse((400, 1), 
            type_of_response = HttpResponse,
            type_of_content  = int)
        self.assertResponse(DEFAULT_STATUS_CODE, 
            type_of_response = HttpResponse,
            type_of_content  = str)
    
    def test_dict(self):
        value = {'foo': date.today()}
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = True)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = True)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = False)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = False)
        assert response3.content == response4.content
        assert response1.content == response3.content
    
    def test_list(self):
        value = ['foo', date.today()]
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = True)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = True)
        assert response3.content == response4.content
        assert response1.content == response3.content
    
    def test_generator(self):
        value = (date.today() for i in range(9))
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        value = (date.today() for i in range(9))
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        assert response1.content == response2.content
        value = (date.today() for i in range(9))
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        value = (date.today() for i in range(9))
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        assert response1.content != response3.content
    
    def test_valuesset(self):
        value = User.objects.values()
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        assert response3.content == response4.content
        assert response1.content != response3.content
    
    def test_queryset(self):
        value = User.objects.all()
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        assert response3.content == response4.content
        assert response1.content != response3.content
    
    def test_related_manager(self):
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(content_type=content_type, codename='change_user')
        self.user.user_permissions.add( permission )
        value = self.user.user_permissions
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            basic_serialization = False)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        assert response3.content == response4.content
        assert response1.content != response3.content
    
    def test_model_instance(self):
        value = self.user
        response1 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = False)
        response2 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            basic_serialization = False)
        assert response1.content == response2.content
        response3 = self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        response4 = self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = str,
            basic_serialization = True)
        assert response3.content == response4.content
        assert response1.content != response3.content

    def test_file(self):
        self.assertResponse((400, open(__file__)), 
            type_of_response = FileResponse,
            type_of_content  = str)
        self.assertResponse(open(__file__), 
            type_of_response = FileResponse,
            type_of_content  = str)
    
    def test_iterator(self):
        self.assertResponse((400, iter(range(9))), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(iter(range(9)), 
            type_of_response = JSONResponse,
            type_of_content  = list)
    
    def test_object(self):
        self.assertResponse((400, type('X', (object,),{})), 
            type_of_response = HttpResponse,
            type_of_content  = str)
        self.assertResponse(type('X', (object,),{}), 
            type_of_response = HttpResponse,
            type_of_content  = str)
    