import email
from unicodedata import name

from django.forms import PasswordInput
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import TestSerializer, CreateUserSerializer, PersonDataSerializer
from rest_framework.response import Response
from user.models import CustomUser
from .models import PersonData, MatcherRulesConfig
from .default_rules import default_rules
from .utilities import PersonMatcher
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import make_password

class TestAPIView(APIView):
    serializer_class = TestSerializer

    def get(self,request, *_, **__):
        user_info = request.user
        print(user_info)
        return Response({'success':'true', 'info':'oldu bea','user':user_info})

    def post(self, *_, **__):

        return Response({'success':'true', 'info':'oldu bea'})

#This class is for user endpoint. It handles user creation
class CreateUserAPIView(APIView):
    serializer_class = CreateUserSerializer
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


    #TODO: Add new functionality here
    def get(self,request, *_, **__):
        user_info = CustomUser.objects.all()
        print(user_info)
        return Response({'success':'true'})

    def post(self, *_, **__):

        name = self.request.data['name']
        username = self.request.data['username']
        email = self.request.data['email']
        password = self.request.data['password']
        password = self.validate_password(password)
        try:
            user = CustomUser()
            user.name = name
            user.username = username
            user.email = email
            user.password = password
            user.save()
        except Exception as e:
            return Response({'success':'false', 'info':'please correct the entered fields or change the username'})

        
        return Response({'success':'true'})


#This class is for Person endpoint. It handles Person Creation
class PersonAPIView(ListAPIView):
    serializer_class = PersonDataSerializer

    def get_queryset(self):
        persons = PersonData.objects.all()
        return persons

    def post(self, *_, **__):

        person_info = PersonDataSerializer(data= self.request.data)
        person_info.is_valid(raise_exception=True)
        person_info.save()
        
        return Response({'success':'true'})

#This class is for Person endpoint. It handles Person Creation
class PersonMatcherAPIView(ListAPIView):
    serializer_class = PersonDataSerializer

    @method_decorator(cache_page(60*60*2))
    def get_queryset(self):
        persons = PersonData.objects.all()
        return persons

    def post(self, *_, **__):
        person_info = PersonDataSerializer(data= self.request.data)
        person_info.is_valid(raise_exception=True)
        matcher = PersonMatcher(person_info)
        match_status = matcher.run()
        match_status_percentage = '%'+ str(match_status)
        return Response({'success':'true','match_status_percent':match_status_percentage})
