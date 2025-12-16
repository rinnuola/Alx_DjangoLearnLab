# posts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, like_post, unlike_post 
# Ensure all views are imported

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
# Register comments under a router for /comments/ access
router.register(r'comments', CommentViewSet, basename='comment') 

urlpatterns = [
    # Router URLs (e.g., /posts/, /posts/1/, /comments/)
    path('', include(router.urls)),
    
    # Feed URL
    path('feed/', FeedView.as_view(), name='user-feed'),
    
    # Like/Unlike URLs - must be placed after router includes if using generic PKs
    path('posts/<int:pk>/like/', like_post, name='like_post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike_post'),
]