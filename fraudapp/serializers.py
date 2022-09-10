from rest_framework import serializers, exceptions
from user.models import CustomUser
from .models import PersonData


"""
class CreateAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email','password')
"""

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email','password')

class TestSerializer(serializers.Serializer):
        image_data = serializers.CharField(required=False, default=None)
        json_data = serializers.JSONField()


class PersonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonData
        fields = ('first_name','last_name','date_of_birth', 'id_number')


        