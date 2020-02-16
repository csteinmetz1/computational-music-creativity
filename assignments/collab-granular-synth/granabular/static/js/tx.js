$(function(){
    var form = $('form');
    $('#myRange').on('change mouseup', function(){
        $.ajax({
            type: "POST",
            url: form.action,
            data: form.serialize(),
        }).done(function(res){
            //do something with the response from the server
        });
    });
});