
    
    var apigClient = apigClientFactory.newClient({
        apiKey: 'JrpYBWv1LN84o8dww5o9x6Kq5hHIrD456zIadAkI'
      });
      
    var params = {
        // This is where any modeled request parameters should be added.
        // The key is the parameter name, as it is defined in the API in API Gateway.
      };
      
    var additionalParams = {
        // If there are any unmodeled query parameters or headers that must be
        //   sent with the request, add them here.
      };
    
    var input = document.getElementById("msg");
    // Access the form element...
    input.addEventListener("keyup", function(event){
        if (event.keyCode === 13) {
            // event.preventDefault();
            var time = new Date().toLocaleTimeString('en-US', { hour12: false, 
                hour: "numeric", 
                minute: "numeric"});

            $("#res").append('<div class="chat-message clearfix"><div class="chat-message-content clearfix"><span class="chat-time">'+time+'</span><h5>User</h5><p>'+String($('#msg').val())+'</p></div></div><hr>');
            $("#res").scrollTop($("#res")[0].scrollHeight);
            var body = {
            "messages": [
            {
                "type": "string",
                "unstructured": {
                "id": "0",
                "text": $('#msg').val(),
                "timestamp": String(new Date())
                }
                }
            ]
            };
        document.getElementById('msg').value='';

        apigClient.chatbotPost(params, body)
            .then(function(result){
            console.log(result);
            console.log(result["data"]["body"]);
            $("#res").append('<div class="chat-message clearfix"><div class="chat-message-content clearfix"><span class="chat-time">'+time+'</span><h5>Chatbot</h5><p>'+result["data"]["body"]+'</p></div></div><hr>');
                //This is where you would put a success callback
            $("#res").scrollTop($("#res")[0].scrollHeight);
            }).catch( function(result){
                //This is where you would put an error callback
                console.log("error happens somewhere");
                console.log(result);
            });
        }
    });

    $('#live-chat header').on('click', function() {
		$('.chat').slideToggle(300, 'swing');
		$('.chat-message-counter').fadeToggle(300, 'swing');
	});

	$('.chat-close').on('click', function(e) {
		//e.preventDefault();
		$('#live-chat').fadeOut(300);
    });