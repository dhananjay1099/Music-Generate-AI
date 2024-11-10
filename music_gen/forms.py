from django import forms

class MusicGenerationForm(forms.Form):
    prompt = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Describe the music you want...'}))
    duration = forms.IntegerField(min_value=5, max_value=300, initial=30, help_text="Duration in seconds")