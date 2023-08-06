$("#btn_facturar").on("click",function (){
	var ticket_id = $("#ticket_id").val();
  var cliente_id = $("#cliente_id").val();
	var mail_destino = $("#mail_destino").val();

	$.ajax({
            url:'/facturacion/factura_ticket/',
            type : 'GET',
            data:{
              'ticket_id' : ticket_id,
              'cliente_id' : cliente_id,
              'mail_destino' : mail_destino,
            },
            success: function(data){
               $("#pdf_frame").attr("src",data.url);
               setTimeout(function () {   
                    $("#pdf_frame").get(0).contentWindow.print();
                }, 1000);

               setTimeout(function(){
                    window.location.replace('/facturacion/');
               }, 30000);
                          
            },
            error: function(data) {
              alert(data.errors);
            },
          });
});

