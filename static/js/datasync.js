$(document).ready(function(){ 
  if ("WebSocket" in window) {
    var domain = window.location.host
    var ws = new WebSocket("ws://"+domain+"/datasync/");
    
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