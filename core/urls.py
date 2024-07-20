from django.contrib import admin
from django.urls import path
from blog import views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    path('login/', views.login),

    path('posts/', views.PostView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='post_detail'),

    path('comments/', views.CommentView.as_view(), name='comments_list_create'),
    path('comments/<int:pk>/', views.CommentView.as_view(), name='comment_detail'),
    
    path('likes/<int:pk>/', views.LikeView.as_view(), name='posts_likes'),
    path('like/', views.LikeView.as_view(), name='posts_like'),

]
