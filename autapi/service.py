
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from .models import todo
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from .serializer import TodoSerializer
from rest_framework import status



def checkForObject(request, model, data):

    """
    Check whether thw given user exits

    model: Model object

    data: The unique value (primary key or username) of object

    Returns the object if exists else returs None
    
    """
    if str(model) == 'User':
    
        try:
            user = model.objects.filter(username=data)
        
        except:
            return None

        return user
    
    else:

        try:
            job = model.objects.get(pk = data, usrid = request.user.id)
            return job

        except ObjectDoesNotExist:
            
            return None

def getToken(username):

    """
    Create or get auth token for the users

    username: Username from serialized data

    Returns created or retrived authorisation token of the user

    """

    token, created = Token.objects.get_or_create(user = username)
    
    if created:
        token.save()
    return  "Token " + str(token)

    
def getTodoItems(pk):

    """
    Retrive todo items based on logged in user

    :param int pk: primary key of user

    :return Queryset: todo queryset of the user

    """

    return todo.objects.filter(usrid=pk)


def updateTodo(request, pk):

    """
    Update status of a job

    pk: Primary key of the job

    data: Data from request

    Returns string message or Flase if object not found
    """

    job = checkForObject(request, todo, pk)

    if job != None:
    
        jobSerial = TodoSerializer(job, data = request.data)
        if jobSerial.is_valid():
            jobSerial.save()

            message = ["Status updated", status.HTTP_201_CREATED]

            return message
    
    
        message = [jobSerial.errors, status.HTTP_400_BAD_REQUEST]
        return message

    message = ["Job not found", status.HTTP_404_NOT_FOUND]
    return message
        

def saveUser(userdataSerial):

    """
    Saves newly signed up user

    userdataSerial: Serialized data of user details

    """

    user = userdataSerial.save()
    user.password = make_password(userdataSerial.data['password'])
    user.save()