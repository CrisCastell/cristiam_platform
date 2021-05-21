from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import RegistrationSerializer, AccountSerializer
from .models import Account
from .permissions import IsAssigned

# Create your views here.
def home(request):
    return HttpResponse('Hola! Este es el home de Accounts')


@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        account         = serializer.save()
        token           = Token.objects.get(user=account).key
        data['status']  = 'Account successfully created'
        data['data']    = {'email': account.email, 'username': account.username, 'token': token}

    else:
        data = serializer.errors
    

    return Response(data)

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAssigned]