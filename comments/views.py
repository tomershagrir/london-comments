from datetime import datetime

from london.templates import render_to_string
from london.http import JsonResponse
from london.conf import settings
from london.db.utils import get_model

from models import Comment

MODELS_WITH_COMMENTS = getattr(settings, 'MODELS_WITH_COMMENTS', None)

def render_comments(owner):
    model_name = owner._meta.verbose_name
    if MODELS_WITH_COMMENTS is not None and model_name in MODELS_WITH_COMMENTS:
        return render_to_string('comments', {'owner': owner, 'comments': Comment.query().filter(owner=owner)})
    return ""

def post_comment(request):
    try:
        body, model_name, owner_pk = request.POST.values()
        owner_model = get_model("%s.%s" % (MODELS_WITH_COMMENTS[model_name], model_name))
        owner = owner_model.query().get(pk = owner_pk)
        comment = Comment.query().create(owner = owner, body=body, author = request.user)
        return JsonResponse('{"status":"ok", "author":"%(author)s", "body":"%(body)s", "created":"%(created)s"}' % comment)
    except:
        return JsonResponse('{"status":"error"}')