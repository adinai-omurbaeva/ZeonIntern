from rest_framework import serializers
from rest_framework.response import Response
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','first_name', 'last_name', 'email', 'phone','country', 'city','password')