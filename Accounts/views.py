from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner


class ProfileRetrieveUpdateView (generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner,)




