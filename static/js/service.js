document.addEventListener('DOMContentLoaded', function () {
    const audioForm = document.getElementById('audioForm');
    const startRecordingBtn = document.getElementById('startRecording');
    const stopRecordingBtn = document.getElementById('stopRecording');
    const submitBtn = document.getElementById('submit');
    const audioPreview = document.getElementById('audioPreview');
    const audioFormPrice = document.getElementById('audioFormPrice');
    const startRecordingBtnPrice = document.getElementById('startRecordingPrice');
    const stopRecordingBtnPrice = document.getElementById('stopRecordingPrice');
    const submitBtnPrice = document.getElementById('submitPrice');

    let mediaRecorder;
    let audioChunks = [];
    
    let mediaRecorderPrice;
    let audioChunksPrice = [];
  
    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);
    audioForm.addEventListener('submit', handleSubmit);
  
    startRecordingBtnPrice.addEventListener('click', startRecordingPrice);
    stopRecordingBtnPrice.addEventListener('click', stopRecordingPrice);
    audioFormPrice.addEventListener('submit', handleSubmitPrice);

    async function startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
  
        mediaRecorder.ondataavailable = function (e) {
          audioChunks.push(e.data);
        };
  
        mediaRecorder.onstop = function() {
          const audioBlob = new Blob(audioChunks, { 'type' : 'audio/wav' });
          const audioUrl = URL.createObjectURL(audioBlob);
          audioPreview.src = audioUrl;
          submitBtn.disabled = false;
        };
  
        mediaRecorder.start();
        startRecordingBtn.disabled = true;
        stopRecordingBtn.disabled = false;
      } catch (err) {
        console.error('Error accessing microphone:', err);
      }
    }
  
    function stopRecording() {
      mediaRecorder.stop();
      startRecordingBtn.disabled = false;
      stopRecordingBtn.disabled = true;
    }
  
    function handleSubmit(event) {
      event.preventDefault();
  
      const formData = new FormData();
      formData.append('audio', new Blob(audioChunks));
      fetch('https://voice-commerce-two.vercel.app/process_audio', {method: 'POST', body: formData})
      .then(response => response.json())
      .then(data => {
        translatedText = data["translatedText"]
        console.log(translatedText)
        document.querySelector('input[name="product_name"]').value = translatedText;
        audioChunks = [];
      })
      .catch(error => {
        console.error('Error sending audio data:', error);
      });
    }
    async function startRecordingPrice() {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorderPrice = new MediaRecorder(stream);
    
          mediaRecorderPrice.ondataavailable = function (e) {
            audioChunksPrice.push(e.data);
          };
    
          mediaRecorderPrice.onstop = function() {
            const audioBlob = new Blob(audioChunksPrice, { 'type' : 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPreview.src = audioUrl;
            submitBtnPrice.disabled = false;
          };
    
          mediaRecorderPrice.start();
          startRecordingBtnPrice.disabled = true;
          stopRecordingBtnPrice.disabled = false;
        } catch (err) {
          console.error('Error accessing microphone:', err);
        }
      }
    
      function stopRecordingPrice() {
        mediaRecorderPrice.stop();
        startRecordingBtnPrice.disabled = false;
        stopRecordingBtnPrice.disabled = true;
      }
    
      function handleSubmitPrice(event) {
        event.preventDefault();
    
        const formData = new FormData();
        formData.append('audio', new Blob(audioChunksPrice));
    
        fetch('https://voice-commerce-two.vercel.app/process_audio', {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
          const translatedText = data["translatedText"];
          console.log(translatedText);
          document.querySelector('input[name="product_price"]').value = translatedText;
          audioChunksPrice = [];
        })
        .catch(error => {
          console.error('Error sending audio data:', error);
        });
      }

})

var copybtn = document.getElementById("copy-btn");
var link = document.getElementById("link");
copybtn.onclick = function(){
  navigator.clipboard.writeText(link.innerHTML);
  copybtn.innerHTML = "Copied"
  setTimeout(function(){
    copybtn.innerHTML = "Copy"
  }, 2000)
}

// $(function () {
//   $('#myTab li:last-child button').tab('show')
// })
// $('#myTab button').on('click', function (event) { 
//   event.preventDefault()
//   $(this).tab('show')
// })

// $('#myTab button[data-target="#profile"]').tab('show') // Select tab by name
// $('#myTab li:first-child button').tab('show') // Select first tab
// $('#myTab li:last-child button').tab('show') // Select last tab
// $('#myTab li:nth-child(3) button').tab('show') // Select third tab