from django.contrib import admin
from .models import MusicTrack

@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ['id', 'prompt', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['prompt', 'error_message']
    readonly_fields = ['created_at']
