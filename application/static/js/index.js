
function setMenuOptionText(optName){
  document.getElementById("menu-option").innerHTML = optName;
}

function clearMenuOptionText(){
  document.getElementById("menu-option").innerHTML = "";
}

// --------- Set On Mouse Over/Down properties to the menu options -------------

document.getElementById("opt-home").onmouseover = function() {setMenuOptionText("Reset IP")};
document.getElementById("opt-home").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-crypto").onmouseover = function() {setMenuOptionText("Cryptography")};
document.getElementById("opt-crypto").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-scanner").onmouseover = function() {setMenuOptionText("Service Scanner")};
document.getElementById("opt-scanner").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-forensic").onmouseover = function() {setMenuOptionText("Forensics")};
document.getElementById("opt-forensic").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-osint").onmouseover = function() {setMenuOptionText("O.S.I.N.T")};
document.getElementById("opt-osint").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-net").onmouseover = function() {setMenuOptionText("Network Analysis")};
document.getElementById("opt-net").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-social").onmouseover = function() {setMenuOptionText("Social Engineering")};
document.getElementById("opt-social").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-anon").onmouseover = function() {setMenuOptionText("Anon Mode")};
document.getElementById("opt-anon").onmouseout = function() {clearMenuOptionText()};

document.getElementById("opt-help").onmouseover = function() {setMenuOptionText("Help")};
document.getElementById("opt-help").onmouseout = function() {clearMenuOptionText()};
// -----------------------------------------------------------------------------
