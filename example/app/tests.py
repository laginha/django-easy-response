import simplejson
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django_simple_response.http import JSONResponse, FileResponse, is_serializable
from django_simple_response.utils.process import to_http
from django_simple_response.utils import is_tuple
from django_simple_response.consts import *
from datetime import date


class SimpleResponseTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get_or_create(username='username')[0]

    def to_http(self, content, careful, in_depth):
        request = self.factory.get('/')
        return to_http( request, content, 
            careful_serialization = careful, 
            in_depth_serialization = in_depth,
        )

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

    def assertResponse(self, value, type_of_response, type_of_content,
    careful_serialization=CAREFUL_SERIALIZATION, 
    in_depth_serialization=IN_DEPTH_SERIALIZATION):
    
        response = self.to_http(value, careful_serialization, in_depth_serialization)
        self.assertTypeOfResponse( response, type_of_response ) 
        self.assertStatusCode( response, value )    
        self.assertTypeOfContent( response, type_of_content )
    
    #
    # TESTS
    #
    
    def test_home_view(self):
        response = Client().get("/")
        self.assertEqual( response.status_code, 401 )
        self.assertEqual( response.content, "Not authorized" )
    
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
        def not_in_depth_error():
            value = {'foo': ['bar', date.today()]}
            self.assertResponse(value, 
                type_of_response = JSONResponse,
                type_of_content  = dict,
                in_depth_serialization = False)
        def not_careful_error():
            self.assertResponse(value, 
                type_of_response = JSONResponse,
                type_of_content  = dict,
                careful_serialization = False
            )
        value = {'foo': date.today()}
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            in_depth_serialization = False)
        self.assertRaises(TypeError, not_careful_error)
        self.assertRaises(TypeError, not_in_depth_error)
    
    def test_list(self):
        def not_in_depth_error():
            value = ['foo', {'bar':date.today()}]
            self.assertResponse(value, 
                type_of_response = JSONResponse,
                type_of_content  = list,
                in_depth_serialization = False)
        def not_careful_error():
            self.assertResponse(value, 
                type_of_response = JSONResponse,
                type_of_content  = list,
                careful_serialization = False
            )
        value = ['foo', date.today()]
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            in_depth_serialization = False)
        self.assertRaises(TypeError, not_careful_error)
        self.assertRaises(TypeError, not_in_depth_error)
    
    def test_generator(self):
        def generator():
            yield 'foo'
            yield ['bar', date.today()]
            
        def not_in_depth_error():
            self.assertResponse(generator(), 
                type_of_response = JSONResponse,
                type_of_content  = list,
                in_depth_serialization = False)
        def not_careful_error():
            value = (date.today() for i in range(9))
            self.assertResponse(value, 
                type_of_response = JSONResponse,
                type_of_content  = list,
                careful_serialization = False
            )
        value = (date.today() for i in range(9))
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        value = (date.today() for i in range(9))
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list)
        value = (date.today() for i in range(9))
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            in_depth_serialization = False)
        self.assertRaises(TypeError, not_careful_error)
        self.assertRaises(TypeError, not_in_depth_error)
    
    def test_valuesset(self):
        value = User.objects.values()
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            in_depth_serialization = False)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            careful_serialization = False
        )
    
    def test_queryset(self):
        value = User.objects.all()
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            in_depth_serialization = False)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            careful_serialization = False
        )
    
    def test_related_manager(self):
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(content_type=content_type, codename='change_user')
        self.user.user_permissions.add( permission )
        value = self.user.user_permissions
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            in_depth_serialization = False)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = list,
            careful_serialization = False
        )
    
    def test_model_instance(self):
        value = self.user
        self.assertResponse((400, value), 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            in_depth_serialization = False)
        self.assertResponse(value, 
            type_of_response = JSONResponse,
            type_of_content  = dict,
            careful_serialization = False
        )

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
    