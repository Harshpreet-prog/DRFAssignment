from django.db import models
from django.contrib.auth.models import User 


class Post(models.Model):
    title = models.CharField( max_length=30 )
    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    liking_users = models.ManyToManyField( User, blank=True )

    @property
    def likes(self):
        return self.liking_users.count()


class Comment(models.Model):
    post = models.ForeignKey( Post , related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

