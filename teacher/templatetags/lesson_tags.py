from django import template
import re

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """Convert YouTube video URL to embed URL"""
    # Regular expressions to match various YouTube URL formats
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    match = re.match(youtube_regex, url)
    if match:
        video_id = match.group(6)
        return f'https://www.youtube.com/embed/{video_id}'
    return url 