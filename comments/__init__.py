import os

from london.apps.themes.registration import register_template
from london.apps.ajax import site

register_template("comments", mirroring="comments/comments.html")
register_template("comment", mirroring="comments/comment.html")

site.register_scripts_dir('comments', os.path.join(os.path.dirname(__file__), 'scripts'))