from london.apps.sites.models import Site

from views import render_comments

def basic(request):
    return {'render_comments_for': render_comments}