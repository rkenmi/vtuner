$(function(){
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

var ajaxFileUpload = function (data) {
    var xhr = new XMLHttpRequest();
    xhr.responseType = "blob";

		xhr.onload = function(e) {
      var cdis = xhr.getResponseHeader('Content-Disposition');
      var ctype = xhr.getResponseHeader('Content-Type');
      var blob = xhr.response;

      var URL = window.URL || window.webkitURL;
      var downloadUrl = URL.createObjectURL(blob);

      var filename = cdis.split("filename= ");
      filename = filename[1];


      // Hack to fix utf-8 strings; escape encodes %XX, decodeURIComponent decodes utf-8 and %XX
      filename = decodeURIComponent(escape(filename));

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

      $("#msg").text("Ready");
      $("#progressbar").progressbar({
        value: 0
      });
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

    form["custom_val"].value = parseInt(form["custom_val"].value);
    if (!form["mp3file"].value){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").css('color', 'red');
      $("#msg").text("Error: Please choose a .mp3 file.");
      return false;
    }

    if (!form["options"].value){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").css('color', 'red');
      $("#msg").text("Error: Please select a proper ReplayGain option.");
      return false;
    }

    if (form["options"].value == 'custom' && (isNaN(form["custom_val"].value))){
      // Prevents the standard submit event
      e.preventDefault();
      $("#msg").css('color', 'red');
      $("#msg").text("Error: Invalid entry for the custom ReplayGain value. Please enter a number from -25 to 25.");
      return false;
    }else if (form["options"].value == 'custom' && (form["custom_val"].value > 25 || form["custom_val"].value < -25)){
      e.preventDefault();
      $("#msg").css('color', 'red');
      $("#msg").text("Error: Number entry is too high or too low. Please enter a number from -25 to 25.");
      return false;
    }else if (form["options"].value == 'normalize'){
      form["custom_val"].value = null;
    }

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
