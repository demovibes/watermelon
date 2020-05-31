'use strict';

// define global functions
var high_id = 0;

// this one does the countdown to 0 on song time remaining
function countdown(start_millis, duration_millis) {
    // start a 1-second timer
    var clock = document.getElementById('countdown');
    var timer_id = setInterval(tick, 1000);
    function tick() {
        // calculate remaining duration to the nearest second
        var remaining_millis = start_millis + duration_millis - Date.now();
        if (remaining_millis < 500) {
            // kill timer at 00:00
            clearInterval(timer_id);
            remaining_millis = 0;
        }

        // compute new time display
        var remaining_seconds = remaining_millis / 1000;
        var mm = Math.floor(remaining_seconds / 60);
        var s = Math.round(remaining_seconds % 60);
        clock.textContent = mm + ':' + (s < 10 ? '0' : '') + s
    }
}

// long-polling event listener
function serverEvents(url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4) {
        if (this.status == 200) {
          // we should have a json object in response now, handle each event
          high_id = this.response.id;
          for(var i = 0; i < this.response.events.length; i++) {
            var obj = this.response.events[i];
            // get the event time as a Date object
            var event_time = new Date(Date.UTC(obj.timestamp[0], obj.timestamp[1] - 1, obj.timestamp[2], obj.timestamp[3], obj.timestamp[4], obj.timestamp[5], obj.timestamp[6] / 1000));
            //console.log("Parsing event " + obj.id + " (" + event_time + ")");
            //console.log("Diff. between now and time is " + (event_time.getTime() - Date.now()) + ")");

            // switch handler based on event type
            if (obj.type === 'PLAYLIST') {
//              console.log(obj.value);
              // update song title and link
              var song = document.getElementById('now-playing-song');
              //console.log(" . Updating song to " + obj.value.name + " (" + obj.value.link + ")");
              song.innerHTML = obj.value.name;
              song.setAttribute('href', obj.value.link);

              // update song requester
              var user = document.getElementById('now-playing-user');
              //nsole.log(" . Updating user to " + obj.value.username + " (" + obj.value.userlink + ")");
              user.innerHTML = obj.value.username;
              user.setAttribute('href', obj.value.userlink);

              // update song duration
              //console.log(" . Updating timer to " + event_time.getTime() + " -> " + obj.value.duration);
              countdown(event_time.getTime(), obj.value.duration * 1000);
            } else {
              alert(obj.value);
            }
          }
        }
        // need to re-open the connection, wait 1/2 second though
        setTimeout(serverEvents, 500, url);
      }
    };
    if (high_id > 0) {
      xhttp.open("GET", url + "?=" + high_id);
    } else {
      xhttp.open("GET", url);
    }
    xhttp.responseType = "json";
    xhttp.send();
}

function init(event) {
    // get time when page loaded
    var start_millis = Date.now();
    // get time remaining (seconds) from the rendered page
    var clock = document.getElementById('countdown');
    var init_mmss = clock.textContent.split(':', 2);
    var duration_millis = init_mmss[0] * 60000 + init_mmss[1] * 1000;
    // start the clock running
    countdown(start_millis, duration_millis);

    // begin tracking server events
    serverEvents("/events/");
}

// things to launch as soon as the HTML doc is here
window.addEventListener('DOMContentLoaded', (event) => {
    init(event)
});
