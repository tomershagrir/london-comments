from london.apps import admin

from models import Comment

class ModuleComment(admin.CrudModule):
    model = Comment
    exclude = ('owner', 'author')
    readonly_fields = ('created',)
    list_display = ('owner','author','created',)
    
class AppComments(admin.AdminApplication):
    title = 'Comments'
    modules = (ModuleComment,)