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
	});

	$('#send_comment_btn').click(function(){
		var textArea = $('#comment_text');
		if(textArea.val().trim() == "") return;
		
		//TODO: replace with serialize()
		$.post('/comments/post/', {'owner_id': ownerIDInput.val(), 'owner_model': ownerModelInput.val(), 'body': textArea.val()}).success(function(response){
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
			commentForm.hide();
			link.show();
		}).error(function(response){
			response = $.parseJSON(response.responseText);
			alert(response.error);
		});
	});
});