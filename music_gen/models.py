from django.db import models

class MusicTrack(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    prompt = models.CharField(max_length=500)
    duration = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='generated_music/', null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"Track: {self.prompt[:50]}..."