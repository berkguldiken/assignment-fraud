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
from rest_framework.permissions import IsAdminUser, AllowAny
#This class is for user endpoint. It handles user creation
class CreateUserAPIView(APIView):
    serializer_class = CreateUserSerializer
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    # auth and perms are disabled because everyone can create a user ?

    def validate_password(self, value: str) -> str:
        return make_password(value)


    #TODO: maybe add get all users that can be used ony for admin ?
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

     
    def get_queryset(self,  *_, **__):
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

    def get_queryset(self):
        persons = PersonData.objects.all()
        return persons

    def post(self, *_, **__):
        person_info = PersonDataSerializer(data= self.request.data)
        person_info.is_valid(raise_exception=True)
        matcher = PersonMatcher(person_info)
        match_status = matcher.run()
        match_status_percentage = str(match_status)
        return Response({'success':'true','match_status_percent':match_status_percentage})
