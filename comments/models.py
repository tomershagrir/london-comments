from datetime import datetime

from london.utils.safestring import mark_safe
from london.db import models

class Comment(models.Model):
    """
    Stores comments for different content types
    """
    owner = models.ForeignKey(related_name="comments", delete_cascade=True)
    operator = models.Field(null=True, blank=True, default=None)
    author = models.ForeignKey('auth.User', related_name="comments", default=None, blank=True, null=True, delete_cascade=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    body = models.TextField()
    
    def get_content(self):
        return mark_safe(self['body'])
    
    def get_comments(self):
        return Comment.query().filter(owner=self)