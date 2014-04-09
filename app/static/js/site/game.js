$(document).ready(function(){

  var game_tmpl = Hogan.compile($("#game-tmpl").text());
  var messages_tmpl = Hogan.compile($("#messages-tmpl").text());

  function update_game(data, textStatus, jqXHR) {
    if(data.victory){
        window.location = "/victory/";
    } else if(data.failure){
        window.location = "/failure/";
    }
    var game_html = game_tmpl.render(data.game);
    $("#game").html(game_html);
    var messages_html = messages_tmpl.render(data);
    $("#messages").html(messages_html);
  }

  $.getJSON('/game_json/', {}, update_game);

  if(window.location.href.indexOf("play/") > -1) {
      window.onkeydown = function(e) {
        var key = e.keyCode ? e.keyCode : e.which;
        if(e.keyCode < 65){
            return
        } else if (90 < e.keyCode) {
            return
        }

        var form, input;
        form = $("#letter-form");
        input = $("<input></input>");
        input.attr("value", String.fromCharCode(e.keyCode));
        input.attr("type", "hidden");
        input.attr("name", "letter");
        form.append(input);
        $.post('/game_json/', form.serialize(), update_game);
    }
  }
})