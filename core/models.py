from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    college = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    budget = models.IntegerField(blank=True, null=True)
    hobbies = models.TextField(blank=True)  # comma separated
    nationality = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    employment = models.CharField(max_length=255, blank=True)
    daynight = models.CharField(max_length=50, blank=True)
    pref_gender = models.CharField(max_length=50, blank=True)
    room_rules = models.TextField(blank=True)
    pref_schedule = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=50, blank=True)

    @property
    def hobbies_list(self):
        if self.hobbies:
            return [h.strip() for h in self.hobbies.split(',') if h.strip()]
        return []

    @property
    def room_rules_list(self):
        if self.room_rules:
            return [r.strip() for r in self.room_rules.split(',') if r.strip()]
        return []

    def save(self, *args, **kwargs):
        # Clean hobbies and room_rules before saving
        if self.hobbies:
            self.hobbies = ','.join([h.strip() for h in self.hobbies.split(',') if h.strip()])
        if self.room_rules:
            self.room_rules = ','.join([r.strip() for r in self.room_rules.split(',') if r.strip()])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
