from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# These code are for referencing only. They are not used in the project.

# # Create a note
# class NoteListCreate(generics.ListCreateAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         # Give us the user object of the user who is currently logged in
#         user = self.request.user 
#         # Return all the notes that belong to the user who is currently logged in
#         return Note.objects.filter(author=user) 
    
#     def perform_create(self, serializer):
#         # Save the author of the note as the user who is currently logged in
#         if serializer.is_valid():
#             serializer.save(author=self.request.user)
#         else: 
#             print(serializer.errors)
            
# # Delete a note
# class NoteDelete(generics.DestroyAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         user = self.request.user 
#         return Note.objects.filter(author=user) 

# These code above are for referencing only. They are not used in the project.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class TokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

