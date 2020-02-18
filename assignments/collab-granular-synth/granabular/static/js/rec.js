let shouldStop = false;
let stopped = false;
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');


stopButton.addEventListener('click', function() {
  shouldStop = true;
});

const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) {
      console.log(e.data.size);
      recordedChunks.push(e.data);
    }

    if(shouldStop === true && stopped === false) {
      mediaRecorder.stop();
      console.log("stop")
      stopped = true;
    }
  });

  mediaRecorder.addEventListener('stop', function() {
    const audioBlob = new Blob(recordedChunks);
    const link = URL.createObjectURL(audioBlob);
    downloadLink.href = link;
    downloadLink.download = 'test.wav';

    // pack the Blob into a form
    var fd = new FormData();
    fd.append('fname', 'test.wav');
    fd.append('audioData', audioBlob);

    // send download link to the server
    $.ajax({
      type: "POST",
      url: "/upload",
      data: fd,
      processData: false,
      contentType: false
    })
  });

  mediaRecorder.start(1000);
};

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);
