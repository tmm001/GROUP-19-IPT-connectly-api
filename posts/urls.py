from django.urls import path
from .views import UserList, UserUpdate, UserDelete, create_user, PostListCreate, PostDetail, CommentListCreate

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/create/', create_user, name='create-user'),  # Keep as function-based view
    path('users/update/<int:id>/', UserUpdate.as_view(), name='user-update'),
    path('users/delete/<int:id>/', UserDelete.as_view(), name='user-delete'),
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
]