from django.core import exceptions
# from django.core.exceptions import ValidationError
from django.core import exceptions
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import todo
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    #  Serializer for User model

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', )


class LoginSerializer(serializers.Serializer):

    #  Serializer for user login

    username = serializers.CharField()
    password = serializers.CharField(style = {'input-type':'password'})

    def validate(self,data):
        
        """
        Validate the user.

        data: information from post request

        Returns the serialized user object if successfully authenticated else raises validation error

        """

        userName = data.get('username')
        passWord = data.get('password')

        user = authenticate(username = userName, password = passWord)

        if user:
            return user

        else:
            msg = ("invalid credentials ")
            raise exceptions.ValidationError(msg)


class TodoSerializer(serializers.ModelSerializer):

    #  Serializer for todo model

    class Meta:

        model = todo
        fields = ('id', 'job', 'completeBy', 'stat', )


class NewTodoSerializer(serializers.ModelSerializer):

    # usrId = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:

        model = todo
        fields = ('id', 'job', 'completeBy','usrid',)



