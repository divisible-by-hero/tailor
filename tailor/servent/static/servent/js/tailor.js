//Tailor
function build_fab(_key, _url){

    //build fab command
    $('form').on('change', 'select', function(){
        // TODO Account for # too
        if (($(this).val() != '---')){
            $(this).clone().appendTo('.terminal');
        }
    });

    $('#execute').click(function(e){

        e.preventDefault();

        //Create Dialog
    	$('#dashboard-terminal').dialog({
    		modal: true,
    		draggable: false,
    		resizable: false,
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
        var selects = $('.tailor-terminal-select:not(:last-child)');
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
                //console.log(data.responses)
                data.responses.forEach(function(item){
                    $('#dashboard-terminal').append(item.response_html)
                })
            },
    	 });
        //end execute fab command 

    });
}
