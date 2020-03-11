$.fn.serializeObject = function()
{
var o = {};
var a = this.serializeArray();
$.each(a, function() {
    if (o[this.name] !== undefined) {
        if (!o[this.name].push) {
            o[this.name] = [o[this.name]];
        }
        o[this.name].push(this.value || '');
    } else {
        o[this.name] = this.value || '';
    }
});
return o;
};

$(function(){
    var sliderForm = $('#sliderForm');
    $('#myRange').on('input', function(){
        event.preventDefault();
        var jsonText = JSON.stringify($('#sliderForm').serializeObject());
        $.ajax({
            type: "POST",
            dataType : 'json',
            contentType: 'application/json',
            url: sliderForm.action,
            data : jsonText
        }).done(function(res){});
    });

    var keywordForm = $('#keywordForm');
    $('#keywordForm').submit(function(){
        event.preventDefault();
        if (keywordForm.serialize() == "keyword="){
            return 
        }
        var jsonText = JSON.stringify($('#keywordForm').serializeObject());
        $.ajax({
            type: "POST",
            dataType : 'json',
            contentType: 'application/json',
            data : jsonText,
            url: keywordForm.action,
        }).done(function(res){});
    });
});
