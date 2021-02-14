var game_over = false
var level = -1
var board = []

function Point(x,y) {
    return {x:x,y:y}
}

// if v is less then min wrap reflect it to the max size
// if v is greater than max, reflect it to the mind size
// Examples:
//   3 with a min of 0 max of 2 becomes 0
//   -1 with a min of 0 max of 2 becomes 2.
function constrainCircular(v, min, max) {
  if (v < min) {
    return max + v + min
  } else if (v > max - 1) {
    return max - v +
      min
  }
  return v
}

function getAdj(p, size) {
  directions = [1, 0, -1]
  points = []
  for (let i = 0; i < directions.length; i++) {
    for (let j = 0; j < directions.length; j++) {
      adj = Point(p.x + directions[i], p.y + directions[j])
      // don't add without any offset
      if (adj.x == p.x && adj.y == p.y) {
        continue
      }
      adj.x = constrainCircular(adj.x, 0, size.x)
      adj.y = constrainCircular(adj.y, 0, size.y)
      points.push(adj)
    }
  }
  return points;
}

function getBoardLookup(board) {
  lookup = {}
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      letter = board[i][j]
      if (!(letter in lookup)) {
        lookup[letter] = []
      }
      lookup[letter].push(Point(i, j))
    }
  }
  return lookup
}

function getActiveCells(text, board) {
  boardLookup = getBoardLookup(board)
  s = Point(board.length, board[0].length)
  first = text.substring(0, 1)
  histories = []
  if (first in boardLookup) {
    starts = boardLookup[first]
    for (let i = 0; i < starts.length; i++) {
      histories.push({
        path: [starts[i]],
        children: getAdj(starts[i], s)
      })
    }
  }
  pattern = text.substring(1)
  while(histories.length > 0 && pattern.length > 0) {
    next_histories = []
    for(let i=0; i < histories.length; i++) {
      first = pattern.substring(0, 1)
      for(let c = 0; c < histories[i].children.length; c++) {
        p = histories[i].children[c]
        if (board[p.x][[p.y]] === first) {
          hist = { path:Array.from(histories[i].path), children:getAdj(p, s) }
          hist.path.push(p)
          next_histories.push(hist)
        }
      }
    }
    histories = next_histories
    pattern = pattern.substring(1)
  }

  paths = []
  for(let i = 0; i < histories.length; i++) {
    paths.push(histories[i].path)
  }
  return paths
}


function update_status(text) {
  $('#status').text(text);
  setTimeout(function() {
      // clear it back out
      $('#status').text("-");
    },
    1000);
}

function set_cookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function get_cookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
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
    m = Math.floor(remaining / 60)
    $('#time').text(m.toString() + "m");
  } else {
    $('#time').text(Math.floor(remaining).toString() + "s");
  }
}

function updateHint(data) {
  rule_text = data["rule_text"]

  $('#hint').html(
    "<div class='row no-gutters justify-content-center'> <p>" +
    rule_text + "</p> </div>"
  );
}

function checkGameOver(data) {
  if (remaining <= 0) {
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
  for (var i = words.length - 1; i >= 0; i--) {
    if (!(words[i].player in player_to_words)) {
      player_to_words[words[i].player] = {
        "valid": 0,
        "invalid": 0
      }
    }
    if (words[i]['valid']) {
      player_to_words[words[i].player]["valid"] = 1 + player_to_words[words[i].player]["valid"]
      named_words += "<div class='row b'><p id=passed-word>" +
        words[i].text + " - " + words[i].player + "</p></div>"
      passing_words += "<p class='passing_word rounded p-1'>" + words[i].text + " </p>"

    } else {

      player_to_words[words[i].player]["invalid"] = 1 + player_to_words[words[i].player]["valid"]
      failed_words += "<p class='failing_word rounded p-1'>" + words[i].text + " </p>"
    }
  }

  $('#passed_words').html(passing_words);
  $('#failed_words').html(failed_words);
  return player_to_words
}

function updatePlayers(data, player_to_words) {

  str = ""
  players = data["players"]
  for (var i = 0; i < players.length; i++) {
    pass_fail = ""
    if (players[i] in player_to_words) {
      pass_fail = "(<p class='passing_word_count'>" +
        player_to_words[players[i]]["valid"].toString() + " </p>" +
        "/" +
        "<p class='failing_word_count'>" +
        player_to_words[players[i]]["invalid"].toString() + " </p>)"
    }
    str += "<div class='row'><p style='margin-right:5px;margin-left:5px'>" +
      players[i] + "</p>" + pass_fail + "</div>"
  }
  $('#player_list').html(str);

}

function checkGameComplete(data) {

  if (level == -1) {
    level = data["level_index"]
  } else if (data["level_index"] != level) {
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
    data: {
      "game": $("#game_name").val()
    },
    error: function(data) {
      update_status("error" + data);
    },
    success: function(data) {
      updateUserInterface(data)
    }
  });
}

function advance() {
  level_up = new Audio('/static/audio/level_up.m4a');
  play_sound(level_up)
  $('#myModal').modal();
  $('#myModal').on('hidden.bs.modal', function() {
    location.reload()
  });
}
setInterval(function() {
  if (!game_over) {
    updateGame()
  }
}, 750);

function addWord() {
  $.ajax({
    url: "add_word",
    data: {
      "game": $("#game_name").val(),
      "word": $("#word_textbox").val(),
      "player": $("#player").val()
    },
    error: function(data) {
      update_status("error" + data);
    },
    success: function(data) {
      $("#word_textbox").val('')
      if (data["invalid"]) {
        update_status(data['invalid']);
        play_sound(invalid_sound)
      } else if (data["valid"]) {
        update_status("word matched");
        play_sound(valid_sound)
      } else {
        update_status("word didn't match");
        play_sound(invalid_sound)
      }
    }
  });
}

function myFunction() {
  /* Get the text field */
  var copyText = $('#status').text();

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
    set_cookie("sound", "off")
  } else {
    set_cookie("sound", "")
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

function getBoard() {
  $.ajax({
    url: "get_board",
    data: {
      "game": $("#game_name").val()
    },
    error: function(data) {
      update_status("error" + data);
    },
    success: function(data) {
      board = data
    }
  });
}

function turnOffLetters() {
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      letterId = "#letter_" + (i + 1).toString() + "_" + (j + 1).toString()
      $(letterId).removeClass("letter_on").css('opacity', 1);
    }
  }
}

function letterPressed() {

  text = $('#word_textbox').val().toUpperCase()
  paths = getActiveCells(text, board)
  turnOffLetters()
  for (let i =0; i < paths.length; i++) {
    for(let j=0; j < paths[i].length; j++) {
        p = paths[i][j]
        letterId = "#letter_" + (p.x + 1).toString() + "_" + (p.y + 1).toString()
        $(letterId).addClass("letter_on").css('opacity', .33 + (j/(1.0*paths[i].length-1)))
    }
  }
}

var valid_sound, invalid_sound;
var audio_on = (get_cookie("sound")).length == 0

$(document).ready(function() {
  valid_sound = new Audio('/static/audio/valid.m4a');
  valid_sound.volume = .35
  invalid_sound = new Audio('/static/audio/invalid.m4a');

  getBoard()

  set_audio_label(audio_on)

  updateGame()
  $('#word_textbox').keyup(function(e) {
    if (e.which == 13) {
      addWord();
      turnOffLetters();
    } else {
      letterPressed()
    }
  });

  $("#addWordButton").click(function() {
    addWord()
  });
});