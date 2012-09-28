from datetime import datetime

from london.templates import render_to_string
from london.http import JsonResponse
from london.conf import settings
from london.db.utils import get_model

from models import Comment

MODELS_WITH_COMMENTS = getattr(settings, 'MODELS_WITH_COMMENTS', {})
MODELS_WITH_COMMENTS.update({'Comment': 'comments'})

SUBCOMMENT_LEFT_MARGIN = 25

#function to render comments template
def render_comments(theme, owner, list_template='comments', item_template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    model_name = owner._meta.verbose_name
    if model_name in MODELS_WITH_COMMENTS:
        return render_to_string(list_template, {
            'owner': owner,
            'comments': get_comments_html(theme, owner, item_template=item_template, margin=margin),
            })
    return ""

#function to render comments with sub-comments
def get_comments_html(theme, owner, result="", level=0, item_template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    comments = Comment.query().filter(owner=owner)
    for comment in comments:
        result += get_comments_html(theme, comment, get_single_comment_html(comment, level, theme, item_template, margin), level+1, item_template, margin) #recursively render subcomments
    return result  
    
#function to render single comment
def get_single_comment_html(comment, level, theme, template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    return render_to_string(template, {'comment': comment, 'margin': level * margin}, theme=theme)

#function to receive comment posting AJAX request 
def post_comment(request):
    try:
        body = request.POST['body']
        model_name = request.POST['owner_model']
        owner_pk = request.POST['owner_id']

        owner_model = get_model("%s.%s" % (MODELS_WITH_COMMENTS[model_name], model_name))
        owner = owner_model.query().get(pk = owner_pk)
        author = request.user if request.user.is_authenticated() else None
        comment = Comment.query().create(owner = owner, body=body, author = author)
        return JsonResponse({
            "status":"ok",
            "pk": comment['pk'],
            "author": unicode(comment['author']) if comment['author'] else "Anonymous",
            "body": comment['body'],
            "created": comment['created'].strftime('%Y-%m-%d, %H:%M'),
            })
    except Exception as e:
        response = JsonResponse({"status":"error", "error":str(e).replace('"', '\\"')})
        response.status_code = 500
        return response

