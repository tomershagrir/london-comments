$(document).ready(function(){
	var commentForm = $('#comment_form');
	var ownerIDInput = $('#owner_id');
	var ownerModelInput = $('#owner_model');
	var comments = $('#comments');

	var newCommentHTML = '<div class="comment" style="margin-left:${margin}px;"><b>${author}</b> <i>said</i>: "${comment}" at <i>${date}</i><br/><a class="reply-link" id="${id}">reply</a></div>';
	addToRoot = true;

	comments.delegate('.reply-link, .add-comment', 'click', function(){
		var link = $(this);
		
		commentForm.appendTo(link.parent()).show();
		ownerIDInput.val(OWNER_ID);
		ownerModelInput.val(OWNER_MODEL);
		if(link.hasClass('reply-link')) {
			addToRoot = false;
			link.hide();
			insertAfter = link.parent();
			ownerIDInput.val(link.attr('id'));
			ownerModelInput.val('Comment');
		}
		else insertAfter = comments.children().last();
	});

	$('#send_comment_btn').click(function(){
		var textArea = $('#comment_text');
		if(textArea.val().trim() == "") return;
		
		//TODO: replace with serialize()
		$.post('/comments/post/', {'owner_id': ownerIDInput.val(), 'owner_model': ownerModelInput.val(), 'body': textArea.val()}).success(function(response){
			if(response.status != "ok") return;
			var newCommentMargin = addToRoot ? 0 : parseInt(insertAfter.css('margin-left'))+25;
			$.tmpl(newCommentHTML, {'author': response.author, 
									'comment': response.body, 
									'date': response.created,
									'id': response.pk,
									'margin': newCommentMargin}).insertAfter(insertAfter); // shift subcomment
			
			textArea.val('');
			commentForm.hide();
		}).error(function(response){
			response = $.parseJSON(response.responseText);
			alert(response.error);
		});
	});
});