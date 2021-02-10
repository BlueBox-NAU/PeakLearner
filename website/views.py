from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from api import CommandHandler
from api.Handlers import Hubs
from api.util.PLdb import User

@view_config(route_name='home', renderer='index.html')
def home(request):
    return {}


@view_config(route_name='about', renderer='about.html')
def about(request):
    return {}



@view_config(route_name='newHub', renderer='newHub.html')
def newHub(request):
    return {}


@view_config(route_name='tutorial', renderer='tutorial.html', )
def tutorial(request):
    return {}


# account views
@view_config(route_name='register', renderer='register.html')
def register(request):
    return {}

@view_config(route_name='register', request_method = "POST")
def registerPOST(request):

    email = request.params['email']
    password = request.params['password']
    secret = request.params['secret']

    user = User(email, password)
    user.put(secret)
    test = user.get()
    
    url = request.route_url('login')
    return HTTPFound(location=url)

@view_config(route_name = 'account', renderer = "account.html")
def account(request):
    return{}

@view_config(route_name='login', renderer = "account.html", request_method = "POST")
def loginPOST(request):

    print(request.matchdict)
    email = request.params['email']
    print(email)
    password = request.params['password']

    user = User(email, password)
    secret = user.get()
    
    return {'secret': secret}


@view_config(route_name='login', renderer='login.html')
def login(request):
    return {}