from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note


# This class that allows users to create new User instances through an API endpoint
class CreateUserView(generics.CreateAPIView ):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]


# this class simplifies creating an endpoint to manage note data securely for authenticated users.
class NoteListCreate(generics.ListCreateAPIView):
	serializer_class = NoteSerializer
	permission_classes = [IsAuthenticated]

	# only the notes belonging to the currently authenticated user are returned
	def get_queryset(self):
		user = self.request.user
		return Note.objects.filter(author=user)

	# check if the serializer's data is valid before saving with current user otherwise error
	def perform_create(self, serializer):
		if serializer.is_valid():
			serializer.save(author=self.request.user)
		else:
			print(serializer.errors)

# This class is designed for deleting Note objects that belong to the currently logged-in user
class NoteDelete(generics.DestroyAPIView):
	serializer_class = NoteSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return Note.objects.filter(author=user)


