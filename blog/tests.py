from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Post, Comment


class PostViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)
        
        self.post1 = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author=self.user)
        
        self.post_list_url = reverse('post_list_create')
        self.post_detail_url = lambda pk: reverse('post_detail', kwargs={'pk': pk})

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
        data = {'title': 'Updated Post 1', 'content': 'updated content'}
        response = self.client.put(self.post_detail_url(self.post1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post 1')
        self.assertEqual(response.data['content'], 'updated content')

    def test_delete_post(self):
        response = self.client.delete(self.post_detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())


class CommentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.comment1 = Comment.objects.create(content='Comment 1', post=self.post, author=self.user)
        self.comment2 = Comment.objects.create(content='Comment 2', post=self.post, author=self.user)
        
        self.comment_list_url = reverse('comments_list_create')
        self.comment_detail_url = lambda pk: reverse('comment_detail', kwargs={'pk': pk})

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


class LikeViewTest(APITestCase):
    def setUp(self):
      
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.get_likes_url = lambda pk: reverse('posts_likes', kwargs={'pk': pk})
        self.post_like_url  = reverse('posts_like')


    def test_get_likes(self):
        response = self.client.get( self.get_likes_url(self.post.pk) )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 0)

    def test_like_post(self):
        response = self.client.post( self.post_like_url , {'pk': self.post.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], 1)
        self.assertTrue(self.post.liking_users.filter(pk=self.user.pk).exists())

    def test_get_likes_nonexistent_post(self):
        response = self.client.get('/likes/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found')

    def test_like_nonexistent_post(self):
        response = self.client.post('/like/', {'pk': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found')
