import logging
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import asyncio
from asgiref.sync import async_to_sync
import torch
import torchaudio
import os
from django.conf import settings
from django.apps import apps

logger = logging.getLogger(__name__)

def load_model():
    try:
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
        if not processor or not model:
            raise ValueError("Failed to load model or processor")
        return (model, processor)  # Explicitly create tuple
    except Exception as e:
        logger.error(f"Error in load_model: {e}")
        raise

def generate_music(track_id, prompt, duration):
    try:
        logger.info(f"Starting music generation for track {track_id}")
        model, processor = load_model()
        
        inputs = processor(
            text=[prompt],
            return_tensors="pt",
        )
        
        # Generate the audio
        audio_values = model.generate(**inputs, max_new_tokens=int(duration * 50))
        
        # Convert to audio file and save
        audio_path = os.path.join(settings.MEDIA_ROOT, f'generated_tracks/track_{track_id}.wav')
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        
        # Convert to audio tensor and save
        audio_tensor = audio_values[0, 0].cpu()
        torchaudio.save(audio_path, audio_tensor.unsqueeze(0), sample_rate=32000)
        
        # Get the MusicTrack model dynamically
        MusicTrack = apps.get_model('music_gen', 'MusicTrack')
        track = MusicTrack.objects.get(id=track_id)
        track.status = 'completed'
        track.audio_file = f'generated_tracks/track_{track_id}.wav'
        track.save()
        
        return True, "Success"
    except Exception as e:
        logger.error(f"Error in generation for track {track_id}: {str(e)}")
        # Update track status to failed if there's an error
        try:
            MusicTrack = apps.get_model('music_gen', 'MusicTrack')
            track = MusicTrack.objects.get(id=track_id)
            track.status = 'failed'
            track.error_message = str(e)
            track.save()
        except Exception as db_error:
            logger.error(f"Error updating track status: {db_error}")
        return False, str(e)

async def generate_music_from_non_async_context(track_id, prompt, duration):
    # Call generate_music directly since we're already in an async context
    success, message = await generate_music(track_id, prompt, duration)
    return success, message
