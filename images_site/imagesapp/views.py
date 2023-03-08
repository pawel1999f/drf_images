from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from imagesapp.serializers import UserSerializer
from imagesapp.models import Profile, ImageModel

from .serializers import ImageModelSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from imagesapp.permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all().filter()
    serializer_class = ImageModelSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        IsOwner]
    
    def get_queryset(self):
        user = self.request.user
        return ImageModel.objects.filter(creator=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)