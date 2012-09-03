from london.apps.sites.models import Site

from views import render_comments

def basic(request):
    def render_comment_with_theme(owner):
        return render_comments(getattr(request, 'theme', None), owner)
    return {'render_comments_for': render_comment_with_theme}