$(function(){
    var form = $('form');
    $('#myRange').on('input', function(){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: form.action,
            data: form.serialize(),
        }).done(function(res){});
    });
});