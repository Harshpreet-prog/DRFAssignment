from django.contrib import admin
from django.urls import path
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    path('login/', views.login),

    path('posts/', views.PostView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='post-detail'),

    path('comments/', views.CommentView.as_view(), name='comments-list-create'),
    path('comments/<int:pk>/', views.CommentView.as_view(), name='comment-detail'),

    path('test_token', views.test_token),
]
