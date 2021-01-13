// Function for copying hash code to the clippboard

function text_to_clip(){
  let copyText = document.getElementById("hash-result");
  document.getElementById('textToHash').value = copyText.value;

}


// Flask & Socketio interaction for dynamic pages

const socket = io();

// Hash identifier

socket.on('hash identify', function(hash){
  $('#identify-result').html('<b class="letter-color">Hash type: </b><b>'+hash+'</b>');
});


$('#sendHashToIdentify').on('click', function(){
  socket.emit('hash identify', $('#hashToIdentify').val());
  $('#hashToIdentify').val('');
});

// Text to hash

socket.on('text to hash', function(hash){
  $('#hash-result').html('<b class="letter-color">Generated hash: </b><b>'+hash+'</b>')
});


$('#sendToHash').on('click', function(){
  let hash_type = $('#hashOptions').val();
  let text = $('#textToHash').val();
  let text_hash = text + '[flag]' + hash_type;
  $('#textToHash').val('');
  socket.emit('text to hash', text_hash);

});

// Text to Encode

socket.on('text to encode', function(encode){
  $('#encodedText').html('<b class="letter-color">Generated encoding: </b><b>'+encode+'</b>')
});


$('#sendToEncode').on('click', function(){
  let encoder = $('#encodeOptions').val();
  let text = $('#codeToEncode').val();
  let text_encoder = text + '[flag]' + encoder;
  $('#textToEncode').val('');
  socket.emit('text to encode', text_encoder);

});

// Code to Decode

socket.on('decode code', function(text){
  $('#decodedText').html('<b class="letter-color">Generated encoding: </b><b>'+text+'</b>')
});


$('#sendToDecode').on('click', function(){
  let decoder = $('#decodeOptions').val();
  let code = $('#codeToDecode').val();
  let code_decoder = code + '[flag]' + decoder;
  $('#codeToDecode').val('');
  socket.emit('decode code', code_decoder);

});
