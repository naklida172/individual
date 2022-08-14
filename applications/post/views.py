from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.post.models import Post, Like, Comment, Favorite, Rating
from applications.post.serializers import PostSerializer, CommentSerializer, RatingSerializer


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['date']
    search_fields = ['text', 'owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):
        like_object, _ = Like.objects.get_or_create(user_id=request.user.id, post_id=pk)
        like_object.like = not like_object.like
        like_object.save()
        status = 'liked'

        if like_object.like:
            return Response({'status': status})
        status = 'not liked'
        return Response({'status': status})

    @action(detail=True, methods=['Post'])
    def save(self, request, pk, *args, **kwargs):
        save_object, _ = Favorite.objects.get_or_create(owner_id=request.user.id, post_id=pk)
        save_object.favorite = not save_object.favorite
        save_object.save()
        if save_object.favorite:
            return Response({'status': 'saved'})
        return Response({'status': 'ain`t saved'})

    @action(detail=True, methods=['Post'])
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(post_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data)