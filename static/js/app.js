$(document).ready(function() {

  var is_recording = false;
  var distance_units = "in";

  // Connect to Tello after wifi connection is established
  $("#connect").click(function() {
      $.getJSON("/connect", {}, function(response) {
          if (response.is_connected == true) {
              // This will light up all the buttons
              $('button').prop('disabled', function(i, v) { return !v; });
          }
      });
      
  });

  // Start the video stream
  $("#streamon").click(function() {
      console.log("Sending command: streamon");
      post("/send_command", JSON.stringify({"command": "streamon"}));
      $("#video").attr("src", "/video_stream");
  });
});

// Called when a control command is being issued
function post(url, command) {
  $.ajax({
      url: url,
      data: command,
      type: 'POST',
      contentType: 'application/json'
  }).done(function(data){
      //
  });
}