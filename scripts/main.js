$(document).ready(function() {
	'use strict';


	console.log('ready');

	$('#ask_question_text').on('click',function() {
		$('#ask_question').show().focus();
		$('#ask_question_text').hide();

	});

	$('#submit_button').click(function(e) {
		e.preventDefault();
		var text = $('#question_text').val();
		var hashTags = text.match(/#.+\s*/)[0];
		var question = text.replace(hashTags, '');
		
		return false;
	});


});