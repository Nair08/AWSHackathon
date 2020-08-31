 $(document).ready(function(){
 
$( "#inlineFormCustomSelect" ).change(function() {
var PollutantsArray = ["AQI", "PM2.5","PM10","Ozone", "Nitrogen Dioxide", "Sulfur Dioxide", "Carbon Monoxide"];	
	
 var pollutant = $(".btn-dark").text();
 var year = "";
    $( "select option:selected" ).each(function() {
      year += $( this ).text() + "";
    });

 //when the selected year is other than 2020
	 if(year!="2020") {
		 
		 initGMap(year, pollutant);
		 
	$("[id^=mapdiv]").css({
    "height": "0px", 
    "opacity": "0"
    });
		
	 
	
	$("#mapdiv8").css({
    "height": "500px", 
    "opacity": "1"
    });
	
	}
	//when the selected year is     2020
	else{
		
		$("#mapdiv8").css({
    "height": "0px", 
    "opacity": "0"
    });
		
		var divNumber = PollutantsArray.indexOf(pollutant) +1;
		 
		$("#mapdiv"+divNumber).css({
    "height": "500px", 
    "opacity": "1"
    });
		
	}
});
});