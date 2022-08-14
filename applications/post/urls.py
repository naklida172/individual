
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.post.views import PostView, CommentView

router = DefaultRouter()
router.register('comment', CommentView)
router.register('', PostView)

urlpatterns = [
    path('', include(router.urls)),

]
