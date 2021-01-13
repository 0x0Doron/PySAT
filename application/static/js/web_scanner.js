
var cbImage = document.getElementById("cbImageDownloader");
var cbDocumentsDownloader = document.getElementById("cbDocumentsDownloader");
var cbEmailGathering = document.getElementById("cbEmailGathering");
var cbBruteContent = document.getElementById("cbBruteContent");
var cbInsecureCookies = document.getElementById("cbInsecureCookies");

// init Port scan always

cbImage.checked = true;
$('#scan-loader').hide();
$('#output-tag').hide();


// ----- scan web -----------


function validURL(str) {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(str);
}


const socket = io();

$('#btnScanTarget').on('click', function(){

  if (validURL($('#siteTarget').val())){
    let array = new Array();

    array.push($('#siteTarget').val()); // FIRST PARAMETER ALWAYS THE SITE URL

    if (cbImage.checked){
      array.push('image_downloader');
    }
    if (cbDocumentsDownloader.checked){
      array.push('document_downloader');
    }
    if (cbEmailGathering.checked){
      array.push('email_gathering');
    }
    if (cbBruteContent.checked){
      array.push('brute_content');
    }
    if (cbInsecureCookies.checked){
      array.push('insecure_cookies');
    }

    let params = array.join(':');
    socket.emit('scan web', params);
    $('#scan-loader').show();
  }

    $('#siteTarget').val('');

});

socket.on('finish', function(n){
  $('#scan-loader').hide();
  $('#output-tag').show();
});


socket.on('img scan web', function(result){
  console.log(result);
  let output = '<p class="img-out" id="terminal"><b class="letter-color">PySAT@Terminal#</b> &nbsp;'+result+'</p>'
  $('#terminal').append(output);
});


socket.on('email scan web', function(result){
  console.log(result);
  let output = '<p class="email-out" id="terminal"><b class="letter-color">PySAT@Terminal#</b> &nbsp;'+result+'</p>'
  $('#terminal').append(output);
});


socket.on('insec cookie scan web', function(result){
  console.log(result);
  let output = '<p class="inseccookies-out" id="terminal"><b class="letter-color">PySAT@Terminal#</b> &nbsp;'+result+'</p>'
  $('#terminal').append(output);
});
