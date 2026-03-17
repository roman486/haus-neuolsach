from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_datetime']


class RSVP(models.Model):
    STATUS_CHOICES = [
        ('yes', '✅ Zusage'),
        ('no', '❌ Absage'),
        ('maybe', '❓ Vielleicht'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('event', 'user')  # Jeder User nur 1x pro Event

    def __str__(self):
        return f'{self.user.username} – {self.get_status_display()} ({self.event.title})'
