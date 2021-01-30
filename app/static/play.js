function update_status(text) {
    $('#status').text(text);
    setTimeout( function(){
            // clear it back out
            $('#status').text("");
        },
        1000);
}

var start_time;
function update_time() {
    total_time = 180
    if (!start_time) {
        start_time = new Date();
    }
    diff = new Date() - start_time
    remaining = total_time - diff/1000
    if (remaining > 60) {
        m = Math.floor(remaining/60)
        console.log(m.toString() + "m")
        $('#time').text(m.toString() + "m");

    } else {
        $('#time').text(Math.floor(remaining).toString() + "s");
    }

}
function update_words() {
        $.ajax({
                url: "get_words",
                data: {"game":$( "#game_name" ).val()} ,
                error: function(data) {
                    update_status("error" + data);
                },
                success:function(data) {
                    //console.log(data)
                    str = ""
                    for(var i = 0; i < data.length; i++){
                        if (data[i]['valid']) {
                            str += "<div class='row'><p id=passed-word>" +
                                     data[i].text  +" - " + data[i].player +"</p></div>"
                        } else {
                            str += "<div class='row'><p id=failed-word>" +
                                     data[i].text  +" - " + data[i].player +"</p></div>"
                        }
                    }
                    $('#word_list').html(str);
                }
         });
}
setInterval(function () {
    update_time()
    update_words()
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
        update_words()
    }
    });
}

$(document).ready(function(){
    update_time()
    update_words()
    $('#word_textbox').keypress(function (e) {
      if (e.which == 13) {
        addWord();
      }
    });

    $("#addWordButton").click(function(){
        addWord()
     });
});