from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import SharedCode.Function as Function
from Set5.Challenge36.Challenge36 import Server

# Unhelpful error to stop side channel attacks
generic_error = "Error has occured"

# Yes, very insecure but it is designed to simulate
# a database
passwordDataBase = {
    'JohnDoe': "pa$$word"
}

# Holds the expected next command no and the server object
sessions = {}


def error():
    r = HttpResponse(generic_error)
    r.status_code = 400
    return r

def sessionError(msg, username):

    if username in sessions:
        del sessions[username]
    
    r = HttpResponse(msg)
    r.status_code = 400
    return r

def correctParameters(request, parameters):

    for x in parameters:
        if x not in request.POST:
            return False

    return True

@csrf_exempt
def action(request):
    """
    SRP related actions. Requires users to be logged in.
    Request should include:
        - 'username'
        - 'commandNo'
        - 'data'
    """

    if not correctParameters(request, ['username', 'commandNo', 'data']):
        return error()

    # Sets up and grabs the data
    username, commandNo, data = setup(request)

    # Checks the expected next commandNo
    expectedCommandNo = sessions[username][0]
    serverObject = sessions[username][1]

    if commandNo != expectedCommandNo:

        # Resets the session
        del sessions[username]

        r = HttpResponse("Unexpected command request!")
        r.status_code = 400
        return r

    # STEP 1
    if commandNo == 1:
        return step1(data, username, serverObject)

    if commandNo == 2:
        return step2(data, username, serverObject)

    if commandNo == 3:
        return step3(data, username, serverObject)

    return HttpResponse("OK")

def setup(request): 
    body = dict(request.POST)

    username = body['username'][0]
    commandNo = int(body['commandNo'][0])
    data = body['data']
    
    # Checks for any integers that are being encoded as strings
    # Not a great way of doing it but I can think of a nicer way
    for index, value in enumerate(data):
        try:
            newValue = int(value)
            data[index] = newValue
        except ValueError:
            pass

    # Creates a new session
    if not username in sessions:
        sessions.update({username: [1, Server()]})

    return username, commandNo, data

def step1(data, username, serverObject):

    if not username in passwordDataBase:
        return sessionError("No user exists!", username)

    # Uses local password
    data[-1] = passwordDataBase[username]

    response = serverObject.step1(data)

    # Updates the session
    sessions[username] = [2, serverObject]

    # Generates password and hash values
    serverObject.step2([])

    return HttpResponse(response)

def step2(data, username, serverObject):

    # C -> [S]
    #   Send I, A=g**a % N (a la Diffie Hellman)
    serverObject.step3(data)

    response = serverObject.step4([])

    # S
    #     Generate S = (A * v**u) ** b % N
    #     Generate K = SHA256(S)
    serverObject.step5([])
    
    # Adds data to the header
    r = HttpResponse()
    r['data'] = response

    # Updates the session
    sessions[username] = [3, serverObject]

    return r

def step3(data, username, severObject):
    
    # Changes tag into bytes
    data[0] = data[0].encode('utf-8')

    response = severObject.step6(data)

    # Ends the session
    del sessions[username]

    return HttpResponse(response)