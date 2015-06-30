$(document).ready(function(){ 
  if ("WebSocket" in window) {
    var ws = new WebSocket("ws://localhost:8888/datasync/");
    
    ws.onopen = function() {
      console.log('Seahorse DataSync online');
    };
    
    ws.onmessage = function (evt) {
      
      // WebSocket DataSync to UI
      var json = evt.data;
      msg = JSON.parse(json);
      
      // if (msg['ui_element'] != null) {
      //   $('#ui_element').html(msg['ui_element']);
      // }
    };
    
    ws.onclose = function() {
      console.log('Seahorse DataSync offline');
    };
  } else {
    alert("WebSocket not supported");
  }
});