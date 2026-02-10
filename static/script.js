let keyEvents = [];

const typingArea = document.getElementById("typingArea");

typingArea.addEventListener("keydown", (e) => {
    keyEvents.push({
        key: e.key,
        type: "down",
        time: performance.now()
    });
});

typingArea.addEventListener("keyup", (e) => {
    keyEvents.push({
        key: e.key,
        type: "up",
        time: performance.now()
    });
});
function extractFeatures(events) {
    let dwellTimes = [];
    let flightTimes = [];

    let keyDownTimes = {};

    for (let event of events) {
        if (event.type === "down") {
            keyDownTimes[event.key] = event.time;
        } else if (event.type === "up") {
            if (keyDownTimes[event.key]) {
                dwellTimes.push(event.time - keyDownTimes[event.key]);
            }
        }
    }

    for (let i = 1; i < events.length; i++) {
        if (events[i].type === "down" && events[i-1].type === "up") {
            flightTimes.push(events[i].time - events[i-1].time);
        }
    }

    const avg = arr => arr.length ? arr.reduce((a,b) => a+b, 0) / arr.length : 0;
    const duration = (events[events.length - 1].time - events[0].time) / 1000;

    return {
        avg_dwell: avg(dwellTimes),
        avg_flight: avg(flightTimes),
        typing_speed: events.length / duration
    };
}
function submitTyping() {
    const mode = document.getElementById("mode").value;
    const features = extractFeatures(keyEvents);

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mode: mode,
            features: features
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
        keyEvents = [];
        typingArea.value = "";
    });
}
