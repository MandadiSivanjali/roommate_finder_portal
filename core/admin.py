from django.contrib import admin
from .models import Profile, Message

# Enable full CRUD for Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'budget', 'daynight')  # fields to display in list
    search_fields = ('user__username', 'location', 'employment', 'nationality')  # searchable fields
    list_filter = ('daynight', 'location')  # filters in sidebar
    ordering = ('user',)  # default ordering

# Optional: Register Message model too
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read',)
    ordering = ('-timestamp',)
    