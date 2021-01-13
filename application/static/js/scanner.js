

function setMenuOptionText(optName){
  document.getElementById("menu-opt").innerHTML = optName;
}

function clearMenuOptionText(){
  document.getElementById("menu-opt").innerHTML = '';
}


document.getElementById("opt-radio").onmouseover = function() {setMenuOptionText("Radio Scanner")};
document.getElementById("opt-radio").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-wifi").onmouseover = function() {setMenuOptionText("Wifi Scanner")};
document.getElementById("opt-wifi").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-ports").onmouseover = function() {setMenuOptionText("Server Scanner")};
document.getElementById("opt-ports").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-web").onmouseover = function() {setMenuOptionText("Web Scanner")};
document.getElementById("opt-web").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-video").onmouseover = function() {setMenuOptionText("Video Vigilance Scanner")};
document.getElementById("opt-video").onmouseout = function() {clearMenuOptionText()};
