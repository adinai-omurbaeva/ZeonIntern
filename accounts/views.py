from django.shortcuts import render
import pyrebase
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics
import argparse
from typing import Optional
from firebase_admin import auth
from firebase_admin.auth import UserRecord
import firebase_admin
from rest_framework.response import Response
from .models import MyUser
from .serializers import MyUserSerializer

app = firebase_admin.initialize_app()


# Remember the code we copied from Firebase.
#This can be copied by clicking on the settings icon > project settings, then scroll down in your firebase dashboard
# config={
#     'apiKey': "AIzaSyAQzxFPoStOfRbkL0Ls-x4IVdLK6tG-rJA",
#     'authDomain': "zeoninternship.firebaseapp.com",
#     'projectId': "zeoninternship",
#     'storageBucket': "zeoninternship.appspot.com",
#     'messagingSenderId': "1052448845702",
#     'appId': "1:1052448845702:web:1fcb833d82c35c4a370607",
#     'measurementId': "G-JLWEJXKQV2"
# }

#
class UsersView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        page = auth.list_users()
        ids = []
       
        for user in auth.list_users().iterate_all():
            ids.append(user.email)
        return Response({tuple(ids)})


class AddUserView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_firebase:UserRecord = auth.create_user(email=new_user.email, password = new_user.password)