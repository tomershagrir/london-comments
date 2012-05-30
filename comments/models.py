from datetime import datetime

from london.utils.safestring import mark_safe
from london.db import models

class Comment(models.Model):
    """
    Stores comments for different content types
    """
    owner = models.ForeignKey(related_name="comments")
    author = models.ForeignKey('auth.User', related_name="comments", default=None, blank=True, null=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    body = models.TextField()
    
    def get_content(self):
        return mark_safe(self['body'])