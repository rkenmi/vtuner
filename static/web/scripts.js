$(function(){ // shorthand for $(document).ready(), which runs after DOM is ready.
  $("#progressbar").progressbar({
    value: 0
  });

  $("label input[type='radio']").change(function(){
    if ($(this).hasClass('more'))
      $('input[name="custom_val"]').prop('disabled', false);
    else {
      $('input[name="custom_val"]').prop('disabled', true);
    }
  });

});

function serveFile(filename, blob) {

  var URL = window.URL || window.webkitURL;
  var downloadUrl = URL.createObjectURL(blob);

  if (filename) {
    var a = document.createElement("a");
    console.log(typeof a.download);
    if (typeof a.download === 'undefined'){
      window.location = downloadUrl;
    } else {
      a.href = downloadUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
    }
  } else {
    window.location = downloadUrl;
  }
}

var ajaxFileUpload = function (data) {
    var xhr = new XMLHttpRequest();
    //xhr.responseType = "blob";
    xhr.responseType = "arraybuffer";

		xhr.onload = function(e) {
      var ctype = xhr.getResponseHeader('Content-Type');
      // Save line space by marking text red by default, set to black for normal msgs
      $("#msg").css('color', 'red');

      if (ctype == 'application/download'){
        var cdis = xhr.getResponseHeader('Content-Disposition');

        var blob = new Blob([xhr.response], {type: ctype});

        var filename = cdis.split("filename= ")[1];

        // Hack to fix utf-8 strings; escape encodes %XX, decodeURIComponent decodes utf-8 and %XX
        filename = decodeURIComponent(escape(filename));

        serveFile(filename, blob);

        $("#msg").text("Ready");
        $("#msg").css('color', 'black');
      }else if (ctype == 'application/json'){
        var str = String.fromCharCode.apply(null, new Uint8Array(xhr.response));
        var obj = JSON.parse(str);
        switch(obj.error){
          case 1: $("#msg").text("Error: Please upload a .mp3 file that is within the file size limit (<15 MB).");
            break;
          case 2: $("#msg").text("Error: Invalid file type.");
            break;
          default: $("#msg").text("Unknown error!");
            break;
        }
      }else ;

      // Reset graphical progress bar
      $("#id_mp3file").click();
    };

		xhr.open("POST", djurl, true);
    xhr.upload.onprogress = function (evt) {
      filename = $("#id_mp3file").text();
      $("#msg").css('color', 'black');
      if ((evt.loaded / evt.total) != 1)
  		  $("#msg").text("Uploading " + filename + " : " + ((evt.loaded / evt.total) * 100).toFixed(2) + "%");
      else
		    $("#msg").text("Processing...");
      $("#progressbar").progressbar({
        value: (evt.loaded / evt.total) * 100
      });
    };
    xhr.send(data);
};


var form = document.querySelector("form");

form.addEventListener("submit", function (e) {

    $("#msg").css('color', 'red');
    form["custom_val"].value = parseInt(form["custom_val"].value);
    if (!form["mp3file"].value){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").text("Error: Please choose a .mp3 file.");
      return false;
    }

    if (!form["options"].value){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").text("Error: Please select a proper ReplayGain option.");
      return false;
    }

    if (form["options"].value == 'custom' && (isNaN(form["custom_val"].value))){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").text("Error: Invalid entry for the custom ReplayGain value. Please enter a number from -25 to 25.");
      return false;
    }else if (form["options"].value == 'custom' && (form["custom_val"].value > 25 || form["custom_val"].value < -25)){
      e.preventDefault();
      $("#msg").text("Error: Number entry is too high or too low. Please enter a number from -25 to 25.");
      return false;
    }else if (form["options"].value == 'normalize'){
      form["custom_val"].value = null;
    }
    $("#msg").css('color', 'black');

    var fdata = new FormData(this);
    ajaxFileUpload(fdata);

    // Prevents the standard submit event
    e.preventDefault();
    return false;
}, false);

$("#id_mp3file").click(function(){
  $("#progressbar").progressbar({
    value: 0
  });
});
