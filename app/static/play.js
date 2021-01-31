function update_status(text) {
    $('#status').text(text);
    setTimeout( function(){
            // clear it back out
            $('#status').text("");
        },
        1000);
}

function update_game() {
        $.ajax({
                url: "get_game_data",
                data: {"game":$( "#game_name" ).val()} ,
                error: function(data) {
                    update_status("error" + data);
                },
                success:function(data) {
                    str = ""
                    rule_text = data["rule_text"]

                    $('#hint').html(
                        "<div class='row no-gutters justify-content-center'> <p>" +
                        rule_text +"</p> </div>"
                    );


                    remaining = data["remaining_time"]
                    if (remaining > 60) {
                        m = Math.floor(remaining/60)
                        $('#time').text(m.toString() + "m");

                    } else {
                        $('#time').text(Math.floor(remaining).toString() + "s");
                    }

                    words = data["remaining_words"]
                    $('#word_count').text(words);

                    words = data["words"]
                    for(var i = 0; i < words.length; i++){
                        if (words[i]['valid']) {
                            str += "<div class='row'><p id=passed-word>" +
                                     words[i].text  +" - " + words[i].player +"</p></div>"
                        } else {
                            str += "<div class='row'><p id=failed-word>" +
                                     words[i].text  +" - " + words[i].player +"</p></div>"
                        }
                    }
                    $('#word_list').html(str);
                }
         });
}
setInterval(function () {
    update_game()
}, 1000);

function addWord() {
  $.ajax({
    url: "add_word",
    data: { "game":$( "#game_name" ).val(),
            "word": $( "#word_textbox" ).val(),
            "player": $( "#player" ).val()
            } ,
    error: function(data) {
        update_status("error" + data);
    },
    success:function(data) {
        $( "#word_textbox" ).val('')

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
}

$(document).ready(function(){
    update_game()
    $('#word_textbox').keypress(function (e) {
      if (e.which == 13) {
        addWord();
      }
    });

    $("#addWordButton").click(function(){
        addWord()
     });
});