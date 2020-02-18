let shouldStop = false;
let stopped = false;
let onair = document.getElementById("onair")
let container = document.getElementById("container")

const grabGrain = function() {
  $(onair).fadeIn("slow", function() {
    $(this).show().css({visibility: "visible"});
  });
  $(container).removeClass("normal")
  $(container).addClass("rec")

  stopped = false;
  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
  .then(handleSuccess);
}

const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) {
      //console.log(e.data.size);
      recordedChunks.push(e.data);
    }

    if(recordedChunks.length >= 3 && stopped === false) {
      $(onair).fadeOut("slow", function() {
        $(this).show().css({visibility: "hidden"});
      });
      $(container).removeClass("rec")
      $(container).addClass("normal")
      mediaRecorder.stop();
      console.log("stop recording")
      stopped = true;
    }
  });

  mediaRecorder.addEventListener('stop', function() {
    const audioBlob = new Blob(recordedChunks);
    const link = URL.createObjectURL(audioBlob);

    // pack the Blob into a form
    var fd = new FormData();
    fd.append('fname', 'test.wav');
    fd.append('audioData', audioBlob);

    // send download link to the server
    $.ajax({
      type: "POST",
      url: "/upload",
      data: fd,
      success: function() {console.log("sent grain to server")},
      processData: false,
      contentType: false
    })
  });

  mediaRecorder.start(1000);
  console.log("start recording")

};

// at random interval grab a new grain and send to the server
(function loop() {
    var rand = Math.round(Math.random() * 60000) + 10000;
    console.log("next grain in", rand/1000, "sec");
    setTimeout(function() {
            grabGrain();
            loop();  
    }, rand);
}());