// JavaScript Document


$(document).ready(function(){

	
	var clkBtn = "";
	$('input[type="submit"]').click(function(evt){
		clkBtn = evt.target.id;
	});



	$("#web_scrap").submit(function(e){
		e.preventDefault();


		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
 			data: $(this).serialize(),
 			
			success: function(json){


     			google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawPriceChart);


				function drawPriceChart() {
			
				  	for (i = 1; i < (json.tienda.length + 1); i++){

						  var options = {

						  	title: json.tienda[i-1].toString(),

							chart: {
							  title: 'Prices',
							},

							legend:{textStyle:{fontSize:'8'}},
							tooltip:{textStyle:{fontSize:'12'}},

							vAxis: { 
							    viewWindowMode:'explicit',
							    viewWindow: {
							        min:0
							    }
							},

						    hAxis : { 
						        textStyle : {
						            fontSize: 12 // or the number you want
						        },
						        slantedText: true, 
						        slantedTextAngle: 45 // here you can even use 180 				        
						    }					

						  };

						  	//alert('bye')
						  	//alert(json.precizo.length)
						  	//console.log(json.precizo.length)
						  	//console.log(json.precizo)

		  				    var data = google.visualization.arrayToDataTable(json.precizo[i-1]);
						  	alert(json.tienda[i-1])
							var chart = new google.visualization.ColumnChart(document.getElementById('tienda_' + i));
	    					chart.draw(data, options);
	    				}
				}

				$(window).resize(function(){
				  drawPriceChart();
				});



                
            },
            
		});
	});


	
})

