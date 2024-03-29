from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.Task
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


#This was just an experiment to see if works. This is not used
class Register(CreateAPIView):
    serializer_class = serializers.RegistrationSerializer
    queryset = models.CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, headers=headers)
    
    # def get_serializer(self, *args, **kwargs):
    #     kwargs['context'] = self.get_serializer_context()

    #     if self.action == "list":
    #         fields = ("email", "full_name")
    #         kwargs["fields"] = fields
    
    #     return self.serializer_class(*args, **kwargs)

class UserRegistrationApiView(APIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.RegistrationSerializer
    
    # def get_serializer(self, *args, **kwargs):
    #     kwargs['context'] = self.get_serializer_context()

    #     if self.action == "list":
    #         fields = ("username", "password")
    #         kwargs["fields"] = fields

    #     return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"https://smart-care.onrender.com/patient/active/{uid}/{token}"
            
            
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
        
# class UserRegistrationViewset( viewsets.ModelViewSet):
#     queryset= models.User.objects.all()
#     serializer_class= serializers.RegistrationSerializer
    
class UserLoginApiView(APIView):
    serializer_class= serializers.UserLoginSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data= request.data)
        
        if serializer.is_valid():
            username= serializer.validated_data['username']
            password= serializer.validated_data['password']
            
            user= authenticate(username= username, password=password)
            if user:
                login(request, user)
                return Response("Login Successful")
                
        return Response('Wrong Info. Try again')
    
    
            