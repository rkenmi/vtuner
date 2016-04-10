$(function(){
  $("#progressbar").progressbar({
    value: 0
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

		xhr.open("POST", d_url, true);
    xhr.upload.onprogress = function (evt) {
        filename = $("#id_mp3file").text();
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
