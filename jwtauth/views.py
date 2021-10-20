from django.contrib.auth.models import User

from .services import getNewTokens
from  autapi.serializer import LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication



class Test(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):

        return Response({"message":"welcome"})


class GetToken(TokenObtainPairView):

    def post(self, request):

        credSerial = LoginSerializer(data = request.data)

        if credSerial.is_valid():

            user = User.objects.get(username = credSerial.data['username'])

            token = getNewTokens(user)

            return Response(token)

        return Response(credSerial.errors)
    
# class RefreshToken(APIView):

#     def post(self, request):

#         t = request.data['refresh']

#         v = refreshToken(t)

#         return Response(v)
