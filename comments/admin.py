from london.apps import admin

from models import Comment

class ModuleComment(admin.CrudModule):
    model = Comment
    exclude = ('owner',)
    readonly_fields = ('created',)
    list_display = ('author','owner','created',)
    
class AppComments(admin.AdminApplication):
    title = 'Comments'
    modules = (ModuleComment,)