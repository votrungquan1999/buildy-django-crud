from django.db import models


class Task(models.Model):
    """
    Simple Task model for to-do application.
    
    Fields:
    - title: Task description
    - completed: Completion status (default: False)
    - created_at: Timestamp of creation (auto-generated)
    """
    title = models.CharField(max_length=255, blank=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
