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
        fields = ['title']

    def validate_title(self, value):
        user = self.context['request'].user
        if Category.objects.filter(id=user.id, title=value).exists():
            raise serializers.ValidationError({"message": "This title is already in use."})

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        category = Category.objects.create(
            author=user,
            title=validated_data['title'],
        )

        category.save()

        return category