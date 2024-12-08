from rest_framework import serializers
from .models import *


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'name', 'surname', 'bio', 'birthday', 'residence', 'hobbies', 'photo', 'date_joined', 'friends')
class FindUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'surname', 'bio', 'birthday', 'residence', 'hobbies', 'photo', 'date_joined', 'friends')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__' #('id', 'author', 'title', 'text', 'image', 'create_date', 'update_date')
        # exclude = ('author',)  # Исключаем поле 'author'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comment.all(), many=True).data
        return representation

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'#('from_user', 'to_user', 'status')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'#('id', 'post', 'author', 'text', 'image', 'create_date', 'update_date')
