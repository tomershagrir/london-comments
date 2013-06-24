from datetime import datetime
from pytz import timezone

from london.utils.safestring import mark_safe
from london.utils.timezones import get_utc_now
from london.db import models


class CommentQuerySet(models.QuerySet):
    def by_author(self, author):
        return self.filter(author=author)


class Comment(models.Model):
    """
    Stores comments for different content types
    """
    class Meta:
        query = 'comments.models.CommentQuerySet'

    owner = models.ForeignKey(related_name="comments", delete_cascade=True)
    author = models.AnyField(null=True, blank=True, default=None)
    created = models.DateTimeField(default=get_utc_now, blank=True)
    body = models.TextField()
    
    def get_created_as_timezone(self, tz):
        try:
            created = self['created'].astimezone(timezone(tz))
        except:
            created = self['created']
        return created
        
    def get_content(self):
        return mark_safe(self['body'])
    
    def get_comments(self):
        return Comment.query().filter(owner=self)

    def get_author(self):
        if isinstance(self['author'], dict) and 'pk' in self['author'] and 'class' in self['author']:
            return self['author']['class'].query().get(pk=self['author']['pk'])

        return self['author']