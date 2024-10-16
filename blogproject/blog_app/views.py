from rest_framework import generics, permissions
from .models import Post
from .serilaizers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import PermissionDenied


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.author:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this post.")
