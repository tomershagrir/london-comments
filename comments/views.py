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
def render_comments(owner, list_template='comments', item_template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    print('1', list_template, item_template) # XXX
    model_name = owner._meta.verbose_name
    if model_name in MODELS_WITH_COMMENTS:
        return render_to_string(list_template, {
            'owner': owner,
            'comments': get_comments_html(owner, item_template=item_template, margin=margin),
            })
    return ""

#function to render comments with sub-comments
def get_comments_html(owner, result="", level=0, item_template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    print('2', item_template) # XXX
    comments = Comment.query().filter(owner=owner)
    for comment in comments:
        result += get_comments_html(comment, get_single_comment_html(comment, level, item_template, margin), level+1, item_template, margin) #recursively render subcomments
    return result  
    
#function to render single comment
def get_single_comment_html(comment, level, template='comment', margin=SUBCOMMENT_LEFT_MARGIN):
    print('3', template) # XXX
    return render_to_string(template, {'comment': comment, 'margin': level * margin})

#function to receive comment posting AJAX request 
def post_comment(request):
    try:
        body, model_name, owner_pk = request.POST.values()
        owner_model = get_model("%s.%s" % (MODELS_WITH_COMMENTS[model_name], model_name))
        owner = owner_model.query().get(pk = owner_pk)
        author = request.user if request.user.is_authenticated() else None
        comment = Comment.query().create(owner = owner, body=body, author = author)
        return JsonResponse('{"status":"ok", "pk":"%s", "author":"%s", "body":"%s", "created":"%s"}' % 
                            (comment['pk'], comment['author'] or "Anonymous", comment['body'], comment['created'].strftime('%Y-%m-%d, %H:%M')))
    except Exception as e:
        response = JsonResponse('{"status":"error", "error":"%s"}' % str(e).replace('"', '\\"'))
        response.status_code = 500
        return response
