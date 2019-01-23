from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import SharedCode.Function as Function


# Unhelpful error to stop side channel attacks
generic_error = "Error has occured"

# Yes, very insecure but it is designed to simulate
# a database
passwordDataBase = {
    'JohnDoe' : "password"
}

tokenDataBase = {}

def error():
    r = HttpResponse(generic_error)
    r.status_code = 400
    return r

@csrf_exempt
def login(request):
    """
    Sends login request to recieve cryptographic token. 
    Body should include:
        - 'username'
        - 'password'
    """

    if request.POST:

        # Checks for username password
        if not 'username' in request.POST or \
           not 'password' in request.POST:

            # Error
            r = HttpResponse(generic_error)
            r.status_code = 400
            return r

        username = request.POST['username']
        password = request.POST['password']

        if not username in tokenDataBase:
            # Authenticate
            if username in passwordDataBase and \
                passwordDataBase[username] == password:

                # Random 16byte token
                token = Function.Encryption.AES.randomKeyBase64()
            
                # Adds to logged in database
                tokenDataBase.update({username: token.decode('utf-8')})

                print(tokenDataBase)
                return HttpResponse(token)

            # Authentication error
            return error()
        
        return HttpResponse("User already logged in")

    else:
        return error


@csrf_exempt
def action(request):
    """
    SRP related actions. Requires users to be logged in.
    Request should include:
        - 'token'
        - 'username'
    """

    # Checks for required data
    if not 'token' in request.POST or \
       not 'username' in request.POST:
        return error()

    # Grabs values from the body
    username = request.POST['username']
    token = request.POST['token']

    # Checks user is logged in
    if username not in tokenDataBase:
        return error()

    # Checks for correct token
    if token != tokenDataBase[username]:
        return error()

    return HttpResponse(f"Hello {username}!")