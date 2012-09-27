$(document).ready(function(){
	var commentForm = $('#comment_form');
	var ownerIDInput = $('#owner_id');
	var ownerModelInput = $('#owner_model');
	var comments = $('#comments');
	var link = null;
	var newCommentHTML = '<div class="comment" style="margin-left:${margin}px;"><b>${author}</b> <i>said</i>: "${comment}" at <i>${date}</i><br/><a class="reply-link" id="${id}">reply</a></div>';

	comments.delegate('.reply-link, .add-comment', 'click', function(){
        console.log('delegate'); // XXX
		link = $(this);
		
		commentForm.appendTo(link.parent()).show();
		ownerIDInput.val(OWNER_ID);
		ownerModelInput.val(OWNER_MODEL);
		addToRoot = true;
		insertAfter = null;
		if(link.hasClass('reply-link')) {
			addToRoot = false;
			link.hide();
			insertAfter = link.parent();
			ownerIDInput.val(link.attr('id'));
			ownerModelInput.val('Comment');
		}
		else {
			var childrenComments = comments.children('.comment');
			if(childrenComments.length) insertAfter = childrenComments.last();
		}
		return false;
	});

	$('#send_comment_btn').click(function(){
        comments_send_function(commentForm, '/comments/post/', true, addToRoot, newCommentHTML, link);
	});
});

function comments_send_function(form, url, hideForm, addToRoot, newCommentHTML, link) {
    var textArea = form.find('#comment_text');
    if (textArea.val().trim() == "") return;
    var ownerId = form.find('#owner_id').val();
    var ownerModel = form.find('#owner_model').val();
    var insertAfter = null; // XXX
    
    console.log([form, url, ownerId, ownerModel, hideForm]); // XXX

    //TODO: replace with serialize()
    $.post(url, {'owner_id': ownerId, 'owner_model': ownerModel, 'body': textArea.val()}).success(function(response){
        if(response.status != "ok") return;
        var newCommentMargin = addToRoot ? 0 : parseInt(insertAfter.css('margin-left'))+25;
        var newComment = $.tmpl(newCommentHTML, {'author': response.author, 
                                'comment': response.body, 
                                'date': response.created,
                                'id': response.pk,
                                'margin': newCommentMargin}); // shift subcomment
        
        if(insertAfter) newComment.insertAfter(insertAfter)
        else newComment.prependTo(comments);
        
        textArea.val('');
        if (hideForm) form.hide();
        if (link) link.show();
    }).error(function(response){
        response = $.parseJSON(response.responseText);
        alert(response.error);
    });
}

