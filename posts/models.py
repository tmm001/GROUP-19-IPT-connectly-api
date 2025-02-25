from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    TEXT = "text"
    # Add other choices as you expand
    POST_TYPE_CHOICES = [
        (TEXT, "Text"),
    ]

    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPE_CHOICES,
        default=TEXT,
    )

    class Meta:  # Add this Meta class
        app_label = 'posts'

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # Add this Meta class
        app_label = 'posts'

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"