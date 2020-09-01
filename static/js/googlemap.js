// JavaScript Document
      "use strict";

let map, popup, Popup, popup2;
/** Initializes the map and the custom popup. */

function initGMap(year, pollutant) {
var ajaxresponse;
var i=1;
pollutant = pollutant.replace(/\s+/g, '');
map = new google.maps.Map(document.getElementById("map8"), {
  center: {
	lat: -33.9,
	lng: 151.1
  },
  zoom: 0
});
        /**
         * A customized popup on the map.
         */

class Popup extends google.maps.OverlayView {constructor(position, content) {
super();
this.position = position;
content.classList.add("popup-bubble"); // This zero-height div is positioned at the bottom of the bubble.

  if( content.innerHTML >100)
  content.classList.add("badhealth");  
  if( content.innerHTML >70 && content.innerHTML <100)
  content.classList.add("normalhealth");  
  if( content.innerHTML <40 )
  content.classList.add("goodhealth"); 


const bubbleAnchor = document.createElement("div");
bubbleAnchor.classList.add("popup-bubble-anchor");

bubbleAnchor.appendChild(content); // This zero-height div is positioned at the bottom of the tip.


this.containerDiv = document.createElement("div");
this.containerDiv.classList.add("popup-container");
this.containerDiv.appendChild(bubbleAnchor); // Optionally stop clicks, etc., from bubbling up to the map.

Popup.preventMapHitsAndGesturesFrom(this.containerDiv);
}
/** Called when the popup is added to the map. */

onAdd() {
this.getPanes().floatPane.appendChild(this.containerDiv);
}
/** Called when the popup is removed from the map. */

onRemove() {
if (this.containerDiv.parentElement) {
  this.containerDiv.parentElement.removeChild(this.containerDiv);
}
}
/** Called each frame when the popup needs to draw itself. */

draw() {
const divPosition = this.getProjection().fromLatLngToDivPixel(
  this.position
); // Hide the popup when it is far out of view.

const display =
  Math.abs(divPosition.x) < 4000 && Math.abs(divPosition.y) < 4000
	? "block"
	: "none";

if (display === "block") {
  this.containerDiv.style.left = divPosition.x + "px";
  this.containerDiv.style.top = divPosition.y + "px";
}

if (this.containerDiv.style.display !== display) {
  this.containerDiv.style.display = display;
}
}
}
	// ajax code
	//  ajaxresponse  = [ [-33.866,151.196, 120] , [-33.866,150.196, 10], [-33.866,152.196, 85] ]
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
		
   // this.responseText;
   // ajaxresponse  = [ [-33.866,151.196, 120] , [-33.866,150.196, 10], [-33.866,152.196, 85] ]
    ajaxresponse = JSON.parse(this.responseText);
    ajaxresponse = Array.from(ajaxresponse);
    //console.log(ajaxresponse);

         ajaxresponse.forEach(function (item, index) {
  console.log(item, index);
 var maindiv = document.getElementById("content");
   var clndiv = maindiv.cloneNode(true);


         clndiv.setAttribute("Id", "content" + index.toString());
         clndiv.innerHTML = item[2];

         document.getElementById("content").appendChild(clndiv);
         popup = new Popup(new google.maps.LatLng(item[0], item[1]), clndiv);

         popup.setMap(map);


});


    }
  };
  xhttp.open("GET", "/getresults?year="+year+"&pollutant="+pollutant, true);
  xhttp.send();






}


 