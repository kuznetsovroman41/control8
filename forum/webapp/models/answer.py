from django.db import models
from django.contrib.auth import get_user_model
from ..models.thread import Thread

User = get_user_model()

class Answer(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer to {self.topic.title} by {self.author.username}'
