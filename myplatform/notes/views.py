from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import NoteSerializer, CategoryListSerializer, CategoryCreateSerializer
from .models import Category, Note
from accounts.models import Account
import base64
from django.core.files.base import ContentFile
import json
from django.http import JsonResponse
from rest_framework import viewsets, generics
from .permissions import IsAssigned

# Create your views here.


class AllNotesList(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAssigned]

    def get_queryset(self):
        queryset = Note.objects.all()
        querysetFiltered = queryset.filter(author=self.request.user.id)
        querysetFilteredAndSorted = querysetFiltered.order_by('-created_date')
        query = self.request.GET.get('nombre', '')
        return querysetFilteredAndSorted



class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAssigned]



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createNote(request):
    data = json.loads(request.body)
    author          = request.user
    image           = data['image']

    if image:
        format, imgstr  = image.split(';base64,')
        ext             = format.split('/')[-1]

        dataImg         = ContentFile(base64.b64decode(imgstr), name=f'{author.username}- casjfjsl.' + ext)
    else:
        dataImg = image

    category = Category.objects.get(pk=1)

    note = Note(author=author, image=dataImg, category=category, title=data['title'], body=data['body'])
    note.save()
    
    return Response({"status":"note created succesfully"})


class AllCategoriesList(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [IsAssigned]

    def get_queryset(self):
        queryset = Category.objects.all()
        querysetFiltered = queryset.filter(author=self.request.user.id)
        querysetFilteredAndSorted = querysetFiltered.order_by('-created_date')
        return querysetFilteredAndSorted

# class CreateCategory(generics.CreateAPIView):
#     serializer_class = CategoryCreateSerializer
#     permission_classes = [IsAssigned]


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createCategory(request):
    data = json.loads(request.body)
    author          = request.user
    category = Category(author=author, title=data['title'])
    category.save()
    
    return Response({"status":"Category created succesfully"})