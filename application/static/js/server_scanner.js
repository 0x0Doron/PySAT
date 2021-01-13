
var cbIPGPS = document.getElementById("cbIPGPS");
var rbHigh = document.getElementById("rbHigh");
var rbLow = document.getElementById("rbLow");

// initial values

cbIPGPS.checked = false;
rbHigh.checked = true;
$('#scan-loader').hide();
$('#exportScanInfo').hide();
$('#opText').hide();


function IPGPS_active() {
  return cbIPGPS.checked;
}

function getConectivity(){
  if (rbHigh.checked) { return '0.5'; } // 0.5 and 1.5 is the socket defaulttimeout
  return '1.5';
}

// sockets

const socket = io();


// recieve response
socket.on('scan server', function(result){
  $('#scan-loader').hide();

  if (result.includes('Error')){
    $('#scan-info').html(result);
  }

});


// time

socket.on('time', function(time){
  $('#scan-loader').hide();
  $('#scan-info').html('<b class="letter-color">Scan time: ' + time + ' seconds </b>');
});

// threads

socket.on('threads', function(n){
  $('#scan-info').html($('#scan-info').html() + '<b class="letter-color">with ' + n + ' active threads</b>');
});

// ports

function port_parser(ports){
  var array = ports.split(':');
  return array
}


// banner

socket.on('banner', function(b){

  $('#opText').show();
  $('#exportScanInfo').show();

  let array = b.split('[flag]');
  $('#totalPorts').html(array.length.toString());

  for (var i = 0; i < array.length; i++){
    let port_banner = array[i].split('[banner]');
    console.log(port_banner);
    $('#portList').html($('#portList').html() +
          '<li class="list-group-item d-flex justify-content-between lh-condensed darky">'+
                '<div>' +
                  '<h6 class="my-0 letter-color"><b>Port ' + port_banner[0] +'</b></h6><br>'+
                  '<p class="description">'+port_banner[1]+'</p>'+
                '</div>'+
                '<span class="text-muted" ></span>'+
              '</li>'
    );
  }

});

// send target
// DATA FORMAT IS: target:IPGS:h/l OR target:h/l

$('#btnScanTarget').on('click', function(){
  var data = $('#target').val()+':';

  if (IPGPS_active()){
      data += 'ipgps:';
  }

  data += getConectivity();

  socket.emit('scan server', data);
  $('#scan-loader').show();
  $('#target').val('');

  host = data.split(':')[0]
  $('#target-info').html('<b class="letter-color">'+host+'</b>');
});

// IPGS

socket.on('ipgps', function(lat_long){
  var lat_long_array = lat_long.split(':');

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: parseFloat(lat_long_array[0]), lng: parseFloat(lat_long_array[1]) },
    zoom: 7,
  });
});


// DISPLAYING THE MAP

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 44.397, lng: -50.644 },
    zoom: 8,
  });
}
