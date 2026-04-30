let keyEvents = [];
const typingArea = document.getElementById("typingArea");
const visualizer = document.getElementById("rhythmVisualizer");
const ctx = visualizer.getContext("2d");

// Track for visualizer smooth paint
let paintX = 0;

typingArea.addEventListener("keydown", (e) => {
    if (e.repeat) return; // Prevent OS auto-fire

    const time = performance.now();
    keyEvents.push({ key: e.key, type: "down", time: time });

    // Draw Key press start
    ctx.fillStyle = "rgba(59, 130, 246, 0.8)";
    ctx.fillRect(paintX, 10, 4, 20);
});

typingArea.addEventListener("keyup", (e) => {
    const time = performance.now();
    keyEvents.push({ key: e.key, type: "up", time: time });

    // Draw flight gap distance
    paintX = (paintX + 8) % visualizer.width;
    if (paintX < 8) ctx.clearRect(0, 0, visualizer.width, visualizer.height); // clear on wrap
});

// Resets visualizer canvas
function resetVisualizer() {
    ctx.clearRect(0, 0, visualizer.width, visualizer.height);
    paintX = 0;
}

// Math Utility
const avg = arr => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
const std = arr => {
    if (arr.length < 2) return 0;
    const mean = avg(arr);
    return Math.sqrt(arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / arr.length);
};
const median = arr => {
    if (arr.length === 0) return 0;
    const sorted = [...arr].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

// Target Digraphs (N-Graphs) to extract specifically based on target sentence
const TARGET_DIGRAPHS = ["th", "he", "qu", "ic", "ck", "br", "ro", "ow", "wn", "fo", "ox", "ju", "um", "mp", "ps", "ov", "ve", "er", "la", "az", "zy", "do", "og"];

function extractAdvancedFeatures(events) {
    let dwellTimes = [];
    let flightTimes = [];
    let keyDownTimes = {};
    let backspaceCount = 0;
    let totalDownKeys = 0;

    let digraphLatencies = {};
    TARGET_DIGRAPHS.forEach(dg => digraphLatencies[dg] = []);

    let sequence = []; // Track sequence of pressed characters

    for (let event of events) {
        if (event.type === "down") {
            totalDownKeys++;
            if (event.key === "Backspace") backspaceCount++;

            if (event.key.length === 1) {
                sequence.push({ char: event.key.toLowerCase(), time: event.time });
            }

            if (!keyDownTimes[event.key]) {
                keyDownTimes[event.key] = event.time;
            }
        } else if (event.type === "up") {
            if (keyDownTimes[event.key]) {
                const dwell = event.time - keyDownTimes[event.key];
                dwellTimes.push(dwell);
                delete keyDownTimes[event.key];
            }
        }
    }

    // Flight Times between consecutive downs
    for (let i = 1; i < events.length; i++) {
        if (events[i].type === "down" && events[i - 1].type === "up") {
            flightTimes.push(events[i].time - events[i - 1].time);
        }
    }

    // Digraph Analysis: Extract latency between sequential keydowns of specific pairs
    for (let i = 1; i < sequence.length; i++) {
        const char1 = sequence[i - 1].char;
        const char2 = sequence[i].char;
        const pair = char1 + char2;

        if (TARGET_DIGRAPHS.includes(pair)) {
            const pairLatency = sequence[i].time - sequence[i - 1].time;
            digraphLatencies[pair].push(pairLatency);
        }
    }

    // Natural Rhythm Filtering
    const maxDwell = Math.max(...dwellTimes, 0);
    const maxFlight = Math.max(...flightTimes, 0);

    if (maxFlight > 1500) {
        throw new Error("Natural Rhythm Anomaly: Pauses exceeded 1.5 seconds. Please type naturally.");
    }
    if (maxDwell > 1000) {
        throw new Error("Natural Rhythm Anomaly: Unnatural dwell time detected.");
    }

    const duration = events.length > 0 ? (events[events.length - 1].time - events[0].time) / 1000 : 1;
    const typing_speed = totalDownKeys / duration; // Keys per second

    if (typing_speed > 18) {
        throw new Error("Natural Rhythm Anomaly: Typing speed physically impossible. Bot detected.");
    }

    const error_rate = totalDownKeys > 0 ? backspaceCount / totalDownKeys : 0;

    let finalFeatures = {
        avg_dwell: avg(dwellTimes),
        std_dwell: std(dwellTimes),
        median_dwell: median(dwellTimes),
        avg_flight: avg(flightTimes),
        std_flight: std(flightTimes),
        median_flight: median(flightTimes),
        typing_speed: typing_speed,
        error_rate: error_rate
    };

    // Collapse digraph arrays to their averages and map to output expected by Python
    TARGET_DIGRAPHS.forEach(dg => {
        // If the user made a typo and missed a digraph, we use 0 or global average flight.
        // Using global average flight serves as a fallback.
        finalFeatures[`L_${dg}`] = digraphLatencies[dg].length > 0
            ? avg(digraphLatencies[dg])
            : avg(flightTimes);
    });

    return finalFeatures;
}

function updateProgressRing(sampleCount) {
    const ringFill = document.getElementById("ringFill");
    const countDisplay = document.getElementById("sampleCountDisplay");

    // Circle circumference = 2 * PI * 24 ≈ 150.7
    const circumference = 150.7;
    const count = Math.min(Math.max(sampleCount, 0), 10);

    // Dash offset calculates how much of the ring is hidden
    const offset = circumference - (count / 10) * circumference;
    ringFill.style.strokeDashoffset = offset;

    countDisplay.innerText = `${count} / 10`;

    // Change color on completion
    if (count >= 10) {
        ringFill.style.stroke = "var(--success)";
    } else {
        ringFill.style.stroke = "var(--accent-glow)";
    }
}

function showResult(message, isSuccess, probability = null) {
    const resBox = document.getElementById("resultBox");
    resBox.className = isSuccess ? "result-success" : "result-error";

    let htmlContent = `<div>${message}</div>`;
    if (probability !== null) {
        htmlContent += `<div class="prob-score">Match Probability: ${probability}%</div>`;
    }

    resBox.innerHTML = htmlContent;
}

function processBiometrics() {
    const mode = document.getElementById("mode").value;
    const username = document.getElementById("username").value.trim();
    const btn = document.getElementById("submitBtn");

    document.getElementById("resultBox").style.display = "none";

    if (!username) {
        showResult("Identity Core completely empty. Please enter an ID.", false);
        return;
    }

    if (keyEvents.length < 20) {
        showResult("Insufficient keystroke data. Please complete the sentence.", false);
        return;
    }

    let features;
    try {
        features = extractAdvancedFeatures(keyEvents);
    } catch (e) {
        showResult(e.message, false);
        keyEvents = [];
        typingArea.value = " ";
        resetVisualizer();
        return;
    }

    btn.disabled = true;
    btn.innerText = "Analyzing Rhythm...";

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, username, features })
    })
        .then(async res => {
            const data = await res.json();
            return { ok: res.ok, data };
        })
        .then(({ ok, data }) => {
            if (!ok) {
                showResult(data.message, false, data.probability);
                return;
            }

            showResult(data.message, true, data.probability);

            if (data.sample_count !== undefined) {
                updateProgressRing(data.sample_count);
            }

            keyEvents = [];
            typingArea.value = "";
            resetVisualizer();
        })
        .catch(err => {
            showResult("System failure check logs.", false);
            console.error(err);
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerText = "Process Biometrics";
        });
}
