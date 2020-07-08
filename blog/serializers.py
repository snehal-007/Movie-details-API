from rest_framework import serializers
from .models import MovieCategory , MoviePost
from django.contrib.auth.models import User 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = ['id','title','created_at']

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = MoviePost     
        fields = ['id','title','rating','release_year','owner','created_at']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=MoviePost.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']