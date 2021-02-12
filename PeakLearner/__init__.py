from pyramid.config import Configurator
from pyramid.request import Request

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow

from website.users.Users import USERS

class RootFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

class UserFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        user = USERS[key]
        user.__parent__ = self
        user.__name__ = key
        return user

def groupfinder(userid, request):
    user = USERS.get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]


def main(global_config, **settings):
    config = Configurator(settings=settings)

    authn_policy = AuthTktAuthenticationPolicy(
        'seekrit',
        callback=groupfinder,
    )
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootFactory)

    # Front end page
    config.add_route('home', '')
    config.add_route('about', '/about/')
    config.add_route('jbrowse', '/jbrowse/')
    config.add_route('newHub', '/newHub/')
    config.add_route('tutorial', '/tutorial/')
    config.add_static_view(name='tutorial/static', path='website:static/tutorial')
    config.add_route('uploadHubUrl', '/uploadHubUrl/')
    config.add_route('jobs', '/jobs/')
    config.add_route('jobInfo', '/jobs/info/')
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.scan('website.views')

    # account routes
    config.add_route('register', '/register/')
    config.add_route('login', '/login/')
    config.add_route('success', '/success/', factory=UserFactory)
    config.add_route('logout', '/logout/')

    config.add_route('api', '/api/')
    config.add_route('hubInfo', '/{user}/{hub}/info/')
    config.add_route('hubData', '/{user}/{hub}/data/{handler}')
    config.add_route('trackData', '/{user}/{hub}/{track}/{handler}/')
    config.add_static_view(name='/{user}/{hub}', path='jbrowse:jbrowse')

    config.scan('api.views')

    return config.make_wsgi_app()
