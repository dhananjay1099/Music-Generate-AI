from django.shortcuts import render
from django.http import JsonResponse
from .models import MusicTrack
from .music_generator import generate_music
import threading
import logging

logger = logging.getLogger(__name__)

def generate_music_async(track_id, prompt, duration):
    try:
        logger.info(f"Starting async generation for track {track_id}")
        success, message = generate_music(track_id, prompt, duration)
        track = MusicTrack.objects.get(id=track_id)
        track.status = 'completed' if success else 'failed'
        track.error_message = '' if success else message
        track.save()
        logger.info(f"Async generation completed for track {track_id}: {message}")
    except Exception as e:
        logger.error(f"Error in async generation for track {track_id}: {str(e)}")
        track = MusicTrack.objects.get(id=track_id)
        track.status = 'failed'
        track.error_message = str(e)
        track.save()

def generate_music_view(request):
    if request.method == 'POST':
        try:
            prompt = request.POST.get('prompt')
            duration = int(request.POST.get('duration', 30))
            
            # Create track with pending status
            track = MusicTrack.objects.create(
                prompt=prompt,
                duration=duration,
                status='pending'
            )
            
            # Start generation in background
            thread = threading.Thread(
                target=generate_music_async,
                args=(track.id, prompt, duration)
            )
            thread.daemon = True  # Make thread daemon so it doesn't block shutdown
            thread.start()
            
            return JsonResponse({
                'status': 'success', 
                'track_id': track.id,
                'message': 'Music generation started'
            })
            
        except Exception as e:
            logger.error(f"Error in view: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    # Get all tracks for display, ordered by creation date (newest first)
    tracks = MusicTrack.objects.all().order_by('-created_at')
    return render(request, 'music_gen/generate.html', {'tracks': tracks})

def track_status(request, track_id):
    track = MusicTrack.objects.get(id=track_id)
    return JsonResponse({
        'status': track.status,
        'audio_url': track.audio_file.url if track.audio_file else None
    })

def check_status(request, track_id):
    try:
        track = MusicTrack.objects.get(id=track_id)
        return JsonResponse({
            'status': track.status,
            'error_message': track.error_message
        })
    except MusicTrack.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Track not found'
        }, status=404)