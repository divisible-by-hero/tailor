//Tailor
function build_fab(_key, _url){
    
    //build fab command
    $('form').on('change', 'select:last-child', function(){
        // TODO Account for # too
        if (($(this).val() != '---')){
            $(this).clone().appendTo('.tailor-fab-container');
        }
    });

    $('#execute').click(function(e){

        e.preventDefault();

        //Create Dialog
    	$('#tailor-terminal').dialog({
    		modal: true,
    		draggable: true,
    		resizable: true,
    		width: 640,
    		height: 480,
    		title: "Terminal",
    		buttons: {
    			Ok: function() {
    				$( this ).dialog( "close" );
    			}
    		}
    	});

        //Create POST Data object
        post_data = {
            "hosts": [],
            "commands": [],
            "api_key": _key,
        }
        
        //Get tailor selects, all but last child (----)
        //Create Command objects
        var selects = $('.tailor-fab-select:not(:last-child)');
        $.each(selects, function(index, item){
            task = { 'command': $(item).children('option:selected').val(), 'params': [] }
            post_data['commands'].push(task);
        })

        //Make the async call
        //Display responses in dialog
    	$.ajax({
    		type: "POST",
    		timeout: 600000,
    		url: _url,
    		dataType: 'json',
    		data: JSON.stringify(post_data),
            success: function(data){
                data.responses.forEach(function(item){
                    $('#tailor-terminal').append(item.response_html)
                })
            },
    	 });
        //end execute fab command 

    });
}
