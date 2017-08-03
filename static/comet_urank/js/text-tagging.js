console.log('ENTRA');

var sentence_values = {};

var onSentenceValueChanged = function($elem, val){
	// update object
	var cdc_id = $elem.attr('for');
	var is_col_desc = val === 'yes' ? true : false;
	sentence_values[cdc_id] = {
		cdc_id : cdc_id,
		is_col_desc : is_col_desc
	};
	// Change bg color
	var bgColor = is_col_desc ? 'rgba(0,200,0,.5)' : 'rgba(200,0,0,.5)';
	$elem.css('background-color', bgColor);

	console.log(sentence_values[cdc_id]);
}


$('.checkbox').change(function() {
	$(this).prop('checked', 'checked');	// necessary if clicked on label instread of radio button
	var radioBtnGroupId = '#' + $(this).attr('for');
	var $elem = $(radioBtnGroupId);
	var val = $(this).val();
	onSentenceValueChanged($elem, val);	
});

$('.lbl-radio').click(function(){
	var $parent = $(this).parent()
	var $checkbox = $parent.find('.checkbox')
	$checkbox.trigger('change');
});

// Submit assessed sentences
$('#btn-save').click(function(evt){
	var data = [];
	Object.keys(sentence_values).forEach(function(cdc_id) {
		data.push(sentence_values[cdc_id]);
	});
	var dataToSend = { data : JSON.stringify(data)};
	console.log(dataToSend);
	$.ajax({
		url : '../update_col_desc_man/',
		type: 'POST',
	    // contentType: 'application/json; charset=utf-8',
	    data : dataToSend
	})
	.done(function(){
		console.log('success');
		window.location.href = '/comet_urank/text_tagging/' //+new_from_index+'/'+new_to_index
	})
	.fail(function(jqXHR, textStatus, errorThrown){
		console.log(errorThrown);
	});
});



