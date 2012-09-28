$(document).ready(function(){
	var commentForm = $('#comment_form');
	var ownerIDInput = $('#owner_id');
	var ownerModelInput = $('#owner_model');
	var comments = $('#comments');
	var link = null;
	var newCommentHTML = '<div class="comment" style="margin-left:${margin}px;"><b>${author}</b> <i>said</i>: "${comment}" at <i>${date}</i><br/><a class="reply-link" id="${id}">reply</a></div>';

	comments.delegate('.reply-link, .add-comment', 'click', function(){
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

    function commentCallback(response) {
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
        form.hide();
        link.show();
    }

    function errorCallback(response){
        response = $.parseJSON(response.responseText);
        alert(response.error);
    }

	$('#send_comment_btn').click(function(){
        comments_send_function(commentForm, '/comments/post/', commentCallback, errorCallback);
	});
});

function comments_send_function(form, url, successCallback, errorCallback, extra_params) {
    var textArea = form.find('#comment_text');
    if (textArea.val().trim() == "") return;
    var ownerId = form.find('#owner_id').val();
    var ownerModel = form.find('#owner_model').val();
    var params = {'owner_id': ownerId, 'owner_model': ownerModel, 'body': textArea.val()};
    if (extra_params) {
        for (var k in extra_params)
            params[k] = extra_params[k];
    }

    //TODO: replace with serialize()
    $.post(url, params).success(successCallback).error(errorCallback);
}

