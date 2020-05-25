// define global functions

// this one does the countdown to 0 on song time remaining
function countdown(object) {
    // get time when page loaded
    var start_millis = Date.now();
    // get time remaining (seconds) from the rendered page
    var init_mmss = object.textContent.split(':', 2);
    var duration_millis = init_mmss[0] * 60000 + init_mmss[1] * 1000;

    // start a 1-second timer
    var timer_id = setInterval(countdown, 1000);
    function countdown() {
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
        object.textContent = mm + ':' + (s < 10 ? '0' : '') + s
    }
}

// things to launch as soon as the HTML doc is here
window.addEventListener('DOMContentLoaded', (event) => {
    countdown( document.getElementById('countdown') );
});
