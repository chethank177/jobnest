from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    RESUME = 'Resume'
    JOB_PORTAL = 'Job Portal'
    INTERVIEW = 'Interview'
    COVER_LETTER = 'Cover Letter'
    OTHER = 'Other'
    CATEGORY_CHOICES = [
        (RESUME, 'Resume'),
        (JOB_PORTAL, 'Job Portal'),
        (INTERVIEW, 'Interview'),
        (COVER_LETTER, 'Cover Letter'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.resource.title}' 