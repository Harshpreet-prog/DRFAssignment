from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Post, Comment

class PostViewTests(APITestCase):
    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)
        
        # Create some posts for testing
        self.post1 = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author=self.user)
        
        self.post_list_url = reverse('post-list-create')
        self.post_detail_url = lambda pk: reverse('post-detail', kwargs={'pk': pk})

    def test_get_all_posts(self):
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_single_post(self):
        response = self.client.get(self.post_detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Post 1')

    def test_post_create(self):
        data = {'title': 'Post 3', 'content': 'Content 3'}
        response = self.client.post(self.post_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Post 3')

    def test_put_update_post(self):
        data = {'title': 'Updated Post 1'}
        response = self.client.put(self.post_detail_url(self.post1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post 1')

    def test_delete_post(self):
        response = self.client.delete(self.post_detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())


class CommentViewTests(APITestCase):
    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create posts and comments for testing
        self.post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.comment1 = Comment.objects.create(content='Comment 1', post=self.post, author=self.user)
        self.comment2 = Comment.objects.create(content='Comment 2', post=self.post, author=self.user)
        
        self.comment_list_url = reverse('comments-list-create')
        self.comment_detail_url = lambda pk: reverse('comment-detail', kwargs={'pk': pk})

    def test_get_all_comments(self):
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_comments_for_post(self):
        response = self.client.get(self.comment_list_url + f'?post={self.post.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_create_comment(self):
        data = {'content': 'Comment 3', 'post': self.post.pk}
        response = self.client.post(self.comment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Comment 3')

    def test_delete_comment(self):
        response = self.client.delete(self.comment_detail_url(self.comment1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment1.pk).exists())
