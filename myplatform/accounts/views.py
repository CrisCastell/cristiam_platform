from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .serializers import RegistrationSerializer, AccountSerializer, AccountImageSerializer, ChangePasswordSerializer
from .models import Account
from .permissions import IsAssigned
from django.core.files.base import ContentFile
import base64
from django.conf import settings

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAssigned]

class ChangePasswordView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = [IsAssigned]
    serializer_class = ChangePasswordSerializer


@api_view(['GET'])
def getUserID(request):
    return Response({"id":request.user.id})


@api_view(['GET', 'PUT'])
def accountImage(request):
    user = Account.objects.get(pk=request.user.id)
    
    if request.method == 'GET':
        serializer = AccountImageSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        data   = request.data
        image  = data["profile_image"]
        user   = request.user
        

        if image:
            format, imgstr  = image.split(';base64,')
            ext             = format.split('/')[-1]

            imageFile         = ContentFile(base64.b64decode(imgstr), name=f'{user.username}-profile-pic.' + ext)
            
        else:
            imageFile = image

        newData = { "profile_image": imageFile }
        serializer = AccountImageSerializer(instance=user, data=newData)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': "successfull", "message": "Successfully updated", "data": serializer.data})
        return Response({"message": "Hubo un error"}, status=400)