from django.db import models

class Tweet(models.Model):
    tweet_text = models.TextField()
    sentiment = models.CharField(max_length=10)  # "Positive" or "Negative"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet_text[:50]  # Show first 50 characters
