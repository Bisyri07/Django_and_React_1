from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

class UserSerializer(serializers.ModelSerializer):
	# define metadata
	class Meta:
		model = User
		fields = ["id", "username", "password"]
		extra_kwargs = {"password": {"write_only": True}}

	# create new user
	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


# convert Note object into json format
class NoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = ["id", "title", "content", "created_at", "author"]
		extra_kwargs = {"author": {"read_only": True}}
