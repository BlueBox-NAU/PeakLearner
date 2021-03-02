from pyramid.view import view_config
from api.Handlers import Jobs, Hubs
from api.util import PLdb as db
from api import CommandHandler
import json


@view_config(route_name='jobInfo', renderer='json')
def jobStatus(request):
    return Jobs.getAllJobs({})


@view_config(route_name='jobs', renderer='json')
def jobs(request):
    query = request.matchdict
    if 'GET' == request.method:
        return Jobs.getAllJobs({})
    if 'POST' == request.method:
        return Jobs.JobHandler(query).runCommand(request.method, request.json_body)
    return []

@view_config(route_name = "myHubs", renderer = "myHubs.html")
def myHubs(request):
    userid = request.unauthenticated_userid
    info = Hubs.getHubInfo("jdh553@nau.edu", "TestHub")
    KEY_TUPLES_LOL = Hubs.GET_THE_HUB_KEYS_LOL()
    print("LMFAOOOOOOOOOOOOOOOOOOOOOOOOO", KEY_TUPLES_LOL)
    matching_tuples = list(filter(lambda tuple: tuple[0] == userid, KEY_TUPLES_LOL))
    hubNames = list(map(lambda tuple: tuple[1], matching_tuples))
    print("hubnames: ", hubNames)

    print("Matching_Tuples: ", matching_tuples)
    huburl = info['tracks']
    print("huburl", huburl)
    for i in range(10):
        print("#################################################")
        print("ahhhhhhhhhhhhhhhhhh")
    print(info)
    for i in range(10):
        print("#################################################")
    return{"userid" : userid}

@view_config(route_name='uploadHubUrl', renderer='json')
def uploadHubUrl(request):
    if 'POST' == request.method:
        # TODO: Implement user authentication (and maybe an anonymous user?)
        user = request.unauthenticated_userid
        for i in range(10):
            print("#################################################")
        print(user)
        print("Request:", request)
        for i in range(10):
            print("#################################################")
        
        
        try:
            return Hubs.parseHub({'user': user, 'url': request.json_body['args']['hubUrl']})
        except json.decoder.JSONDecodeError:
            print("request.POST: ", request.POST)
            print("request.POST['hubUrl']: " , request.POST['hubUrl'])
            parsedHub = Hubs.parseHub({'user': user, 'url': request.POST['hubUrl']})
            print("Parsed Hub: ", parsedHub)
            return parsedHub
    return


@view_config(route_name='hubInfo', renderer='json')
def hubInfo(request):
    query = request.matchdict
    return Hubs.getHubInfo(query['user'], query['hub'])


@view_config(route_name='hubData', renderer='json')
def hubData(request):
    query = request.matchdict
    for i in range(10):
        print("#################################################")
    print(query)
    for i in range(10):
        print("#################################################")
    if request.method == 'GET':
        return CommandHandler.runHubCommand(query, request.method)

    elif request.method == 'POST':
        return CommandHandler.runHubCommand(query, request.method, request.json_body)


@view_config(route_name='trackData', renderer='json')
def trackData(request):
    query = request.matchdict
    if 'GET' == request.method:
        return CommandHandler.runTrackCommand(query, request.method)
    if 'POST' == request.method:
        return CommandHandler.runTrackCommand(query, request.method, request.json_body)
    return []


@view_config(route_name='doBackup', renderer='json')
def runBackup(request):
    return db.doBackup()


@view_config(route_name='doRestore', renderer='json')
def runRestore(request):
    if 'POST' == request.method:
        return db.doRestoreWithSelected(request.POST['toRestore'])

    return db.doRestore()
