from django.db import models

class Book(models.Model):
    """
    Unified model to store book information from various sources.
    """
    SOURCE_CHOICES = [
        ('google', 'Google Books API'),
        ('user', 'User Recommendation'),
    ]

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='google')
    source_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  
    title = models.CharField(max_length=255)
    authors = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True, null=True)
    categories = models.JSONField(default=list, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)  
    rating = models.FloatField(blank=True, null=True)  
    publication_date = models.DateField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class UserInteraction(models.Model):
    """
    Model to track interactions with book recommendations without associating with a specific user.
    """
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('comment', 'Comment'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
        default='like'  
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.interaction_type} on {self.book}"