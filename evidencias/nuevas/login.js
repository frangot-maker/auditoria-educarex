/* -=[ login.js ]=- */
function checkCampos() {

    $('#formulario-acceso').validate({
        rules: {
            usuario: { minlength: 1, required: true },
            password: { minlength: 1, required: true }
        },
        messages: { usuario: "", password: "" },
        highlight: function(element) {
            $(element).closest('.form-group').addClass('has-error');
        },
        unhighlight: function(element) {
            $(element).closest('.form-group').removeClass('has-error');
        },
        errorElement: 'span',
        errorClass: 'help-block',
        errorPlacement: function(error, element) {
            if (element.parent('.input-group').length) {
                error.insertAfter(element.parent());
            } else {
                error.insertAfter(element);
            }
        }
    }).form();


    if ($("#formulario-acceso").valid()) {
        $.ajax({
            type: "POST",
            url: BASE_URL + "login/login/login",
            dataType: "JSON",
            data: $("#formulario-acceso").serialize(),
            beforeSend: function () {  $('#btnLogin').html("<span class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span> Validando..."); },        
            complete: function () {  $('#btnLogin').html("Acceder");}, 
            success: function(data) {
                if (data.validacionOK === 0) {
                    $('#divmensajeerror').show();
                    $('#mensajeerror').html("<i class='icon fa fa-ban'></i>" + data.mensaje);
                    $("#divmensajeerror").fadeTo(2000, 500).slideUp(500, function(){
                       $("#divmensajeerror").slideUp(500);
                    });                      
                } else {
                    $('#divmensajeerror').hide();
                    if (data.admin === 1)
                        window.location.replace(BASE_URL + 'admin/admin');
                    else
                        window.location.replace(BASE_URL + 'dashboard');
                }
            }
        });
    }
}




$( "#btnLogin" ).click(function() {
  checkCampos();
});


$( ".close" ).click(function() {
  $('#divmensajeerror').hide();
});


$(document).keypress(function(e) {
    if(e.which == 13) {
        checkCampos();
    }
});

