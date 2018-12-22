function renderTable() {
  $("#time").find("tr:gt(0)").remove();
  $.each(members, function(index, value) {
    var loggedIn = value[5] === "True";
    var row = "<tr id=entry" + index + ">" +
      "<td>" + value[0] + "</td>" +
      "<td class='name'>";
      if (loggedIn) {
        row += "<b>";
      }
      row += value[1];
      if (loggedIn) {
        row += "</b>";
      }
      row += "</td>" +
      "<td>" + (value[2]/3600) + "</td>" +
      "<td>" + value[3] + "</td>" +
      "<td>" + value[4] + "</td>" +
      "</tr>";
    $("#time").append(row);
  });
}

function renderEvents() {
  $.each(events, function(index, value) {
    var li = "<li class='event text-center'>" + value + "</li>";
    $('#events').append(li);
	var selectItem = "";
	if (value === currentEvent) {
	  selectItem = "<option selected>" + value + "</option>";
	}
	else {
	  selectItem = "<option>" + value + "</option>";
	}
	$('#currentEvent').append(selectItem);
  });
  $('#events li').each(function() {
    if ($(this).html() == currentEvent) {
      $(this).toggleClass("active");
    }
  });
}

$(document).ready(function() {
  renderTable();
  renderEvents();

  /////////////////////////////////
  // SocketIO listeners
  /////////////////////////////////

  socket.on('select-event', function(data) {
    members = data;
    renderTable();
  });

  socket.on('toggle-sign-in', function(data) {
	  if (data.enabled === "False") {
	    $('#signIn').attr("value", "Enable Sign-In");
	    $('#signIn').css("color", "#f35f00");
	  }
	  else {
	    $('#signIn').attr("value", "Disable Sign-In");
	    $('#signIn').css("color", "#292b2c");
	  }
  });

  socket.on('register', function(data) {
    if (data.success) {
      $('#newMember').attr("value", "Registered!");
    }
    else {
      $('#newMember').attr("value", "Registration Failed");
    }

    setTimeout(function() {
      $('#newMember').attr("value", "Place Tag");
    }, 3000);
  });

  socket.on('tag-present', function(data) {
    if (data.tag) {
      $('#newMember').attr("value", "Place Tag");
      $('#newMember').attr('disabled', 'disabled');
    }
    else {
      $('#newMember').attr("value", "Register Member");
      var empty = false;
      if ($('#newMember').val() == '') {
        empty = true;
      }
      if (!empty) {
        $('#newMember').removeAttr('disabled');
      }
    }
  });

  //////////////////////////////////
  // SocketIO Action Handlers
  //////////////////////////////////
  $('#events .event').click(function() {
    $(this).toggleClass("active");
    var events = [];
    $('#events .event').each(function(index, value) {
      if ($(value).hasClass("active")) {
        events.push($(value).html());
      }
    });
    socket.emit('select-event', {"events": events});
  });

  $('#signIn').click(function() {
    socket.emit('toggle-sign-in', {});
	});

  $('#newMember').click(function() {
    socket.emit('register', $('#registerMember').serialize());
  });

  $('#newEvent').click(function() {
    var li = "<li class='event text-center'>" + $('#event').val() + "</li>";
    var selectItem = "<option>" + $('#event').val() + "</option>";
    $('#events').append(li);
    $('#currentEvent').append(selectItem);
    socket.emit('new-event', $('#createEvent').serialize());
  });

  $('#currentEvent').change(function() {
    socket.emit('change-event', {'currentEvent': this.value});
  });

  //Tag update scheduler
  setInterval(function() {
    //Check if tag is available for registration
    socket.emit('tag-present', {});
  }, 1000);

  /////////////////////////////////////
  // UI Handlers
  /////////////////////////////////////

  //Search bar listener
  $('#nameSearch').on("input", function(search) {
    var name = $('#nameSearch').val();
    $('#time tr').each(function(index, value) {
      var nameTd = $('#time tr').eq(index).find('.name');
      if (nameTd && index != 0) {
        if (nameTd.html().startsWith(name)) {
          $('#time tr').eq(index).show();
        }
        else if (index != 0){
          $('#time tr').eq(index).hide();
        }
      }
    });
  });

  //Key listeners
  $('#member').keyup(function() {
    var empty = false;
    if ($(this).val() == '') {
      empty = true;
    }
    if (empty) {
      $('#newMember').attr('disabled', 'disabled');
    } else {
      $('#newMember').removeAttr('disabled');
    }
  });
  $('#event').keyup(function() {
    var empty = false;
    if ($(this).val() == '') {
      empty = true;
    }
    if (empty) {
      $('#newEvent').attr('disabled', 'disabled');
    } else {
      $('#newEvent').removeAttr('disabled');
    }
  });
});
