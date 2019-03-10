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

// Access the form element...
$("#submit").on("click",function(event){
  // event.preventDefault();
  $("#res").append("<p>"+$('#msg').val()+"</p>");

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
  
apigClient.chatbotPost(params, body)
  .then(function(result){
    console.log(result);
    $("#res").append("<p>"+result["data"]["body"]+"</p>");
      //This is where you would put a success callback
  }).catch( function(result){
      //This is where you would put an error callback
      console.log("error happens somewhere");
      console.log(result);
  });
});