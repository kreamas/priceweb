
$(document).ready(function(){

	//Tienda

	$("#bTiendaAll").click(function(){
		$("#tienda option").prop('selected', true);
	});

	$("#bTiendaNone").click(function(){
		$("#tienda option").prop('selected', false);
	});


	$("#formTienda").submit(function(e) {
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $(this).serialize(),


			success: function(json){

				$('#mercado').html("");

				for (i = 1; i < (json.mercados.length + 1); i++){
					$("#mercado").append("<option value = '" + json.mercados[i-1] + "' selected>" + json.mercados[i-1] + "</OPTION>");
				}

			},

		});

	});




	//Mercado

	$("#bMercadoAll").click(function(){
		$("#mercado option").prop('selected', true);
	});

	$("#bMercadoNone").click(function(){
		$("#mercado option").prop('selected', false);
	});




	$("#formMercado").submit(function(e) {
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $('#formMercado').serialize(),


			success: function(json){

				$('#familia').html("");

				for (i = 1; i < (json.familias.length + 1); i++){
					$("#familia").append("<option value = '" + json.familias[i-1] + "' selected>" + json.familias[i-1] + "</OPTION>");
				}

			},

		});

	});


	//Familia

	$("#bFamiliaAll").click(function(){
		$("#familia option").prop('selected', true);
	});

	$("#bFamiliaNone").click(function(){
		$("#familia option").prop('selected', false);
	});



	$("#formFamily").submit(function(e) {
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $('#formMercado, #formFamily').serialize(),



			success: function(json){



				$('#brands').html("");

				for (i = 1; i < (json.marcas.length + 1); i++){
					$("#brands").append("<option value = '" + json.marcas[i-1] + "' selected>" + json.marcas[i-1] + "</OPTION>");
				}

			},

		});

	});





	//Marcas

	$("#bBrandsAll").click(function(){
		$("#brands option").prop('selected', true);
	});

	$("#bBrandsNone").click(function(){
		$("#brands option").prop('selected', false);
	});



	$("#formBrands").submit(function(e) {
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $('#formMercado, #formFamily, #formBrands').serialize(),


			success: function(json){

				$('#sku').html("");

				for (i = 1; i < (json.sku.length + 1); i++){
					$("#sku").append("<option value = '" + json.sku[i-1] + "' selected>" + json.sku[i-1] + "</OPTION>");
				}

			},

		});

	});






	//Sku

	$("#bSkuAll").click(function(){
		$("#sku option").prop('selected', true);
	});

	$("#bSkuNone").click(function(){
		$("#sku option").prop('selected', false);
	});



	 $(function() {
	    $( "#initial-date").datepicker({dateFormat: "yy-mm-dd"});
	  });


	 $(function() {
	    $( "#last-date").datepicker({dateFormat: "yy-mm-dd"});
	  });





	$("#consultaPrice").submit(function(e) {
		e.preventDefault();


		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $('#initial-date, #last-date, #chart-style, #measure, #nom-item, #chart-views, #formTienda, #formMercado, #formFamily, #formBrands, #sku').serialize(),




			success: function(json){

				$('#graf-price').html("");
				$('#graf-price').append("<br><br>");
				$('#graf-price').append("<table class = 'columns'>");



				for (i = 1; i < (json.elementos.length + 1); i++){
				//for (i = 1; i < 2; i++){
					//alert(json.elementos[i-1]);
					$("#graf-price").append("<p class = 'tit-chart'>" + json.elementos[i-1] + "</p>");
					$("#graf-price").append("<tr><td style = 'width: 40%;'><div class = 'grafico' id ='" + json.elementos[i-1] + "'></div></td></tr>");
					$("#graf-price").append("<br><br>");
				}

				$('#graf-price').append("</table>");


				// Graficos

     			google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawPriceChart);



				function drawPriceChart() {

					for (i = 1; i < (json.elementos.length + 1); i++){

						var data = google.visualization.arrayToDataTable(json.matriz[i-1]);



						  var options = {

						  	//title: json.tienda[i-1].toString(),

							chart: {
							  title: '',
							},

							pointSize: 12,
							legend:{textStyle:{fontSize:'12'}, position: 'bottom'},
							tooltip:{textStyle:{fontSize:'12'}},

							vAxis: { 
							    viewWindowMode:'explicit',
							    viewWindow: {
							        min:0
							    }
							},

						    //hAxis : { 
						    //    textStyle : {
						    //        fontSize: 12 // or the number you want
						    //    },
						    //    slantedText: true, 
						    //    slantedTextAngle: 0 // here you can even use 180 				        
						    //}					

						  };

						if (json.tchart == 'LINE'){
							var chart = new google.visualization.LineChart(document.getElementById(json.elementos[i-1]));
							chart.draw(data, options);
						} else {

							var chart = new google.visualization.ColumnChart(document.getElementById(json.elementos[i-1]));
							chart.draw(data, options);

						}

					};

				}

				$(window).resize(function(){
				  drawPriceChart();
				});











			},

		});

	});


})


