from django.db import models
from django.contrib.auth.models import User



def get_rank(post_count):
    if post_count >= 200:
        return '👑 Legende'
    elif post_count >= 100:
        return '🧓 Experte'
    elif post_count >= 50:
        return '🧑 Dåmpfplauderer'
    elif post_count >= 20:
        return '🧒 Plaudatåschn'
    elif post_count >= 5:
        return '👶 Springgingale'
    else:
        return '🍼 Rotzpipm'





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} – {"✅ freigeschalten" if self.is_approved else "⏳ ausstehend"}'

    @property
    def display_name(self):
        return self.first_name if self.first_name else self.user.username

    @property
    def post_count(self):
        return self.user.post_set.count()

    @property
    def rank(self):
        return get_rank(self.post_count)
