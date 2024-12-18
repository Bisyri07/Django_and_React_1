from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	# define metadata
	class Meta:
		model = User
		fields = ["id", "username", "password"]
		extra_kwargs = {"password": {"write_only": True}}

	# create new user
	def crate(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user
