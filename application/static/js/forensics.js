
let default_info = "Different utilities for Meta-Data extraction & data analysis";

function setMenuOptionText(optName){
  document.getElementById("menu-opt").innerHTML = optName;
}

function clearMenuOptionText(){
  document.getElementById("menu-opt").innerHTML = default_info;
}


document.getElementById("opt-images").onmouseover = function() {setMenuOptionText("<b class='letter-color'>Utilities for: </b>Image analysis")};
document.getElementById("opt-images").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-pdfs").onmouseover = function() {setMenuOptionText("<b class='letter-color'>Utilities for: </b>PDF analysis")};
document.getElementById("opt-pdfs").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-virus").onmouseover = function() {setMenuOptionText("<b class='letter-color'>Utilities for: </b>Virus analysis")};
document.getElementById("opt-virus").onmouseout = function() {clearMenuOptionText()};
