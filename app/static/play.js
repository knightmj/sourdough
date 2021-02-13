var game_over = false
var level = -1

function update_status(text) {
    $('#status').text(text);
    setTimeout( function(){
            // clear it back out
            $('#status').text("-");
        },
        1000);
}

function set_cookie(cname,cvalue,exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function get_cookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function updateTime(data) {
    remaining = data["remaining_time"]
    if (remaining > 60) {
        m = Math.floor(remaining/60)
        $('#time').text(m.toString() + "m");
    } else {
        $('#time').text(Math.floor(remaining).toString() + "s");
    }
}

function updateHint(data) {
    rule_text = data["rule_text"]

    $('#hint').html(
        "<div class='row no-gutters justify-content-center'> <p>" +
        rule_text +"</p> </div>"
    );
}
function checkGameOver(data) {
    if (remaining <=0) {
        game_over = true
        $("#word_textbox").val('<game over>')
        $("#word_textbox").attr("disabled", "disabled");
        $("#addWordButton").attr("disabled", "disabled");
    }
}

function updateWords(data) {
    remaining_words = data["remaining_words"]
    $('#word_count').text(remaining_words);

    named_words = ""
    passing_words = ""
    failed_words = ""
    words = data["words"]
    player_to_words = {}
    for(var i = words.length-1; i >= 0 ; i--){
        if (!(words[i].player in player_to_words)) {
                player_to_words[words[i].player] = {"valid": 0, "invalid": 0}
         }
        if (words[i]['valid']) {
            player_to_words[words[i].player]["valid"] = 1 + player_to_words[words[i].player]["valid"]
            named_words += "<div class='row b'><p id=passed-word>" +
                     words[i].text  + " - " + words[i].player +"</p></div>"
            passing_words+= "<p class='passing_word rounded p-1'>" + words[i].text +" </p>"

        } else {

            player_to_words[words[i].player]["invalid"] = 1 + player_to_words[words[i].player]["valid"]
            failed_words+= "<p class='failing_word rounded p-1'>" + words[i].text +" </p>"
        }
    }

    $('#passed_words').html(passing_words);
    $('#failed_words').html(failed_words);
    return player_to_words
}

function updatePlayers(data, player_to_words) {

    str =""
    players = data["players"]
    for(var i = 0; i <players.length ; i++){
        pass_fail = ""
        if (players[i] in player_to_words) {
            pass_fail =  "(<p class='passing_word_count'>" +
                         player_to_words[players[i]]["valid"].toString() + " </p>" +
                         "/" +
                         "<p class='failing_word_count'>" +
                         player_to_words[players[i]]["invalid"].toString() +" </p>)"
        }
        str += "<div class='row'><p style='margin-right:5px;margin-left:5px'>" +
                players[i] + "</p>" + pass_fail + "</div>"
    }
    $('#player_list').html(str);

}

function checkGameComplete(data) {

    if (level == -1) {
        level = data["level_index"]
    }
    else if (data["level_index"]  != level){
        advance()
        game_over = true
    }
}

function updateUserInterface(data) {
    updateHint(data)
    updateTime(data)
    checkGameOver(data)
    player_to_words = updateWords(data)
    updatePlayers(data, player_to_words)
    checkGameComplete(data)
}

function updateGame() {
        $.ajax({
                url: "get_game_data",
                data: {"game":$( "#game_name" ).val()} ,
                error: function(data) {
                    update_status("error" + data);
                },
                success:function(data) {
                    updateUserInterface(data)
                }
         });
}
function advance() {
        level_up = new Audio('/static/audio/level_up.m4a');
        play_sound(level_up)
        $('#myModal').modal();
        $('#myModal').on('hidden.bs.modal', function () {
            location.reload()
        });
}
setInterval(function () {
    if (!game_over){
        updateGame()
     }
}, 750);

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
            play_sound(invalid_sound)
        }
        else if (data["valid"]){
            update_status("word matched");
            play_sound(valid_sound)
        }
        else {
            update_status("word didn't match");
            play_sound(invalid_sound)
        }
    }
    });
}

function myFunction() {
  /* Get the text field */
  var copyText =  $('#status').text();

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
}

function play_sound(sound) {
    if (audio_on) {
        // stop if it is already playing
        sound.currentTime = 0;
        sound.play();
    }
}

function audio_toggle() {
    audio_on = (get_cookie("sound")).length == 0
    if (audio_on) {
        set_cookie("sound","off")
    }
    else {
        set_cookie("sound","")
    }
    audio_on = !audio_on
    set_audio_label(audio_on)
}
function set_audio_label(audio_on) {
    if (audio_on) {
        $('#audio_label').html("🔉");
    } else {
        $('#audio_label').html("🔇");
    }
}

var valid_sound, invalid_sound;
var audio_on = (get_cookie("sound")).length == 0

$(document).ready(function(){
    valid_sound = new Audio('/static/audio/valid.m4a');
    valid_sound.volume = .35
    invalid_sound = new Audio('/static/audio/invalid.m4a');

    set_audio_label(audio_on)

    updateGame()
    $('#word_textbox').keypress(function (e) {
      if (e.which == 13) {
        addWord();
      }
    });

    $("#addWordButton").click(function(){
        addWord()
     });
});