function update_status(text) {
    $('#status').text(text);
    setTimeout( function(){
            // clear it back out
            $('#status').text("");
        },
        1000);
}

$(document).ready(function(){
    $("#addWordButton").click(function(){
        $.ajax({
                url: "add_word",
                data: {"game":$( "#game_name" ).val(), "word": $( "#word_textbox" ).val()} ,
                error: function(data) {
                    update_status("error" + data);
                },
                success:function(data) {
                    console.log(data)
                    if (data["invalid"]) {
                        update_status(data['invalid']);
                    }
                    else if (data["valid"]){
                        update_status("word matched");
                    }
                    else {
                        update_status("word didn't match");
                    }
                }
         });
     });
});