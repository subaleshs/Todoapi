
from django.contrib.auth import login
from django.contrib.auth.models import User
from autapi.models import todo
from .serializer import UserSerializer, TodoSerializer, LoginSerializer, NewTodoSerializer
from .service import getToken, getTodoItems, saveUser, updateTodo


from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status



class ListUsers(APIView):

    permission_classes=[AllowAny]

    def get(self, request):

        """
        Get all users (for testing only)

        :param request: HttpRequest object

        :return JSONRespose:json encoded response 

        """

        userList = User.objects.all()

        userListSerial = UserSerializer(userList, many=True)

        return Response(userListSerial.data)



class SignUp(APIView):

    def post(self, request):

        """
        Register new user

        :param request: HttpRequest object

        :return JSONRespose:json encoded response 

        """

        userDataSerial = UserSerializer(data = request.data)
        
        if userDataSerial.is_valid():
    
            saveUser(userDataSerial)
            return Response({'message': 'User created'}, status = status.HTTP_201_CREATED)

        else:
            return Response(userDataSerial.errors, status = status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):

        """
        Logs in the user using the credentials

        :param request: HttpRequest object

        :return JSONRespose:json encoded response with auth token

        """

        credentialSerial = LoginSerializer(data = request.data)

        if credentialSerial.is_valid():

            user = User.objects.get(username = credentialSerial.data['username'])
            token =getToken(user)

            login(request, user)
            
            return Response({"username": str(request.user), "token": token})

        return Response(credentialSerial.errors)


class AddViewTodo(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        """
        Get all the todos of the currently logged in user

        :param request: HttpRequest object

        :return JSONRespose:json encoded response containing the todo, date, and status 

        """

        todolist = getTodoItems(request.user.id)

        todoSerial = TodoSerializer(todolist, many = True)

        return Response(todoSerial.data)


    def post(self,request):

        """
        Post new todo to DB

        :param request: HttpRequest object

        :return JSONRespose:json encoded response containing the todo, date, and status
        
        """


        request.data["usrid"] = request.user.id 
        newTodoSerial = NewTodoSerializer(data = request.data)

        if newTodoSerial.is_valid():

            newTodoSerial.save()

            todoList = getTodoItems(request.user)

            todoListSerial = TodoSerializer(todoList, many = True)

            return Response(todoListSerial.data, status = status.HTTP_201_CREATED )

        return Response(newTodoSerial.errors, status = status.HTTP_400_BAD_REQUEST)


class UpdateTodo(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self,request, itemKey):
        
        """
        Update status of job

        :param request: HttpRequest object

        :param int itemKey: Primary key of job

        :return JSONRespose:json encoded response containing the todo, date, and status
        
        """

        data = request.data

        message = updateTodo(request, itemKey)

        return Response({"message": message[0]}, status = message[1])


class DeleteTodo(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete( self, request, itemKey):

        """
        Delete an item from todo.

        :param requeset: HttpRequest object

        :param int itemKey: Primary key of job

        :return JSONRespose:json encoded response

        """

        todo.objects.get(pk = itemKey).delete()

        return Response({"message": "Job deleted"}, status = status.HTTP_204_NO_CONTENT)

        
