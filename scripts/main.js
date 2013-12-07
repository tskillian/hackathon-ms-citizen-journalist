$(document).ready(function() {
	'use strict';

	//helper function to remove form if a form is already there
	var ifFormRemoveForm = function() {
		if ($('form')) {
			$('form').remove();
		}
	};

	//add text form when ask button is clicked
	$('#ask_button').click(function() {
		ifFormRemoveForm();

		$('#text_area_div').append('<form action="http://citizen-journalist.appspot.com/" method="get" role="form"><div class="form-group"><label for="tags">Please add relevant hash tags</label><input name="tags" type="text" class="form-control" id="tags_input" placeholder="Add one or more tags here"></div><div class="form-group"><label for="question">What do you want asked?</label><input name="question" type="text" class="form-control" id="question_form" placeholder="Insert question here"></div><button class="btn btn-success">Submit</button><button id="cancel_button" type="button" class="btn btn-danger">Cancel</button></form>');

		$('#cancel_button').click(function() {
			event.preventDefault();
			ifFormRemoveForm();
		});
	});

	//add text form when 'I will be talking to' button is clicked
	$('#talk_button').click(function() {
		ifFormRemoveForm();

		$('#text_area_div').append('<form action="http://citizen-journalist.appspot.com/" method="get" role="form"><div class="form-group"><label for="talking_to">Who will you be talking to?</label><input name="talking_to" type="text" class="form-control" id="talking_to_form" placeholder="Insert name(s) here"></div><button class="btn btn-success">Submit</button><button id="cancel_button" class="btn btn-danger">Cancel</button></form>');

		$('#cancel_button').click(function() {
			event.preventDefault();
			ifFormRemoveForm();
		});
	});


});