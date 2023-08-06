var $total = $("#total");
var $subtotal = $("#subtotal");
var $descuento = $("#descuento");
var $descuentop = $("#descuentop");
var $descuento_tp = $("#descuento_tp");
var $total_con_descuento = $("#total_con_descuento");
var moneda_id = $("#select_monedas").val();
var lista_precios_id = $("#select_lista_precios").val();
var lista_articulos_ids = [];
var $row;

$(document).ready(function(){
	$("#id_ventasdocumentodetalle_set-0-articulo_text").addClass('form-control');
	$("input[name*='-unidades']").first().focus();
});

// Funcion que carga el articulo seleccionado en autocomplete
function cargar_articulo($articulo, articulo_id, articulo_nombre){ 
	$articulo.parent().find(".deck.div").attr('style','');
	$articulo.parent().find(".deck.div").html('<span class="div hilight" data-value="'+articulo_id+'"><span style="display: inline;" class="remove div">X</span>'+articulo_nombre+'</span>');
	$articulo.parent().parent().find("select[name*='-articulo']").html('<option selected="selected" value="'+articulo_id+'"></option>');
	$articulo.parent().find("input").hide();
	$articulo.parent().parent().find("select[name*='-articulo']").trigger("change");
	$articulo.parent().show();
	$articulo.parent().parent().show();
}

function foco_detalle(){
	$("[name*='-articulo-autocomplete']").attr("class","form-control");
	$(".delete-row").find("i").attr("class","glyphicon glyphicon-trash");
}


$("input").on("keypress", function(e) {
            /* ENTER PRESSED*/
        if (e.keyCode == 13) {
        	$(this).trigger( "focusout" );
        }
    });

//AL QUITAR EL FOCO DE LA CLAVE
$("input[name*='-clave']").on("focusout",function(){
	var $this = $(this);
	var clave = $this.val();
	if (clave != '')
	{
		$.ajax({
	 	   	url:'/auditacotizacion/articulo_by_clave/',
	 	   	type : 'get',
	 	   	data : {
	 	   		'clave':clave,
	 	   	},
	 	   	success: function(data){
	 	   		if (data.articulo_id == null)
	 	   		{
	 	   			// var sound = document.getElementById("beep-one");
	 	   			// for (var i = 0; i <5; i++) {
	 	   			// 	sound.play();
	 	   			// };
	 	   			// alert("No se encontraron articulos con esta clave");
	 	   			$this.focus();
	 	   			// return false;
	 	   		}
	 	   		else
	 	   		{
	 	   			$row = $this.parent().parent().parent().parent().parent();
	 	   			if ($("input[name*='-clave']").last().val() != "")
	 	   			{
	 	   				lista_articulos_ids = [];
	 	   				// SE CREA LA LISTA CON LOS IDS DE LOS ARTICULOS QUE YA ESTAN EN LOS DETALLES.
	 	   				$("select[name*='-articulo']").each(function(){
	 	   					
	 	   					lista_articulos_ids.push(String($(this).val()));
	 	   				});
						$articulo = $this.parent().parent().find("input[name*='-articulo']");
						cargar_articulo($articulo,data.articulo_id,data.articulo_nombre);
						var articulo_id = String($this.parent().parent().parent().find("select[name*='-articulo']").val());
	 	   				if (lista_articulos_ids.indexOf(articulo_id) >= 0)
	 	   				{
	 	   					$row.parent().find("select[name*='-articulo']").each(function(){
	 	   						if ($(this).val() == articulo_id)
	 	   						{
									var $row_art = $(this).parent().parent().parent().parent().parent();
									var unidades_art = parseFloat($row_art.find("input[name*='-unidades']").val());
									$row_art.find("input[name*='-unidades']").val(unidades_art+parseFloat($("input[name*='-unidades']").last().val()))
									$row.find(".delete-row").trigger("click");
	 	   						};
	 	   					});
	 	   				}
	 	   				else
	 	   				{
							$("input[name*='-clave']").last().attr("disabled",true);
	 	   				}
	 	   				
	 	   				$(".btn-success").trigger("click");
						$("input[name*='-unidades']").last().focus();
						$("input[id*='-articulo_text']").attr('class','form-control');
	 	   			};
	 	   		};
			},
		});
	};
});



$("input").on("focusin",function(){
	$(this).select();
});


$("#crear_documento").on("click",function(){
	var folio_pedido = prompt("¿Que folio tiene el pedido a auditar?");
	if (folio_pedido != null)
	{
		$("#crear_documento").attr("disabled",true);
		var lista = [];
		$("#id_detalles_data").find("tbody tr").each(function(){

			var detalle = []
			var articulo_id = $(this).find("select[name*='-articulo']").val();
			if (articulo_id != null)
			{
				detalle.push(articulo_id[0]);
				var unidades = $(this).find("[name*='-unidades']").val();
				detalle.push(unidades);
				lista.push(detalle);
			};
		});
		$.ajax({
	 	   	url:'/auditacotizacion/crea_documento/',
	 	   	type : 'get',
	 	   	data : {
	 	   		'lista':JSON.stringify(lista),
	 	   		'folio_pedido': folio_pedido,
	 	   	},
	 	   	success: function(data){
	 	   		var documento_folio = data.documento_folio;
	 	   		var existe = data.existe;
	 	   		var modulo = data.modulo;
	 	   		var surtido = data.surtido;
	 	   		if (existe == 1)
	 	   		{
		 	   		if (surtido == '0')
		 	   		{
		 	   			alert("Se Creó la Remisión con folio "+documento_folio);
		 	   			location.reload();
		 	   		}
		 	   		else
		 	   		{
		 	   			alert("Este Pedido ya se encuentra Surtido.");
		 	   		};
		 	   		$("#crear_documento").attr("disabled",false);
	 	   		}
	 	   		else
	 	   		{
	 	   			alert("Pedido no Existe");
	 	   			$("#crear_documento").attr("disabled",false);
	 	   		};
	 	   	},
	 	   	error:function(){
	 	   		alert("Error");
	 	   	},
		});
	};
});