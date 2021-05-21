from rest_framework import serializers
from .models import Category, Note
from accounts.models import Account

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [ 'id', 'title', 'body', 'category', 'image']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [ 'id', 'title']


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'