
const state = {
    curX: 0, curY: 0, curRot: 0,
    tgtX: 0, tgtY: 0, tgtRot: 0,
    eyeL: 1, eyeR: 1, mouthOpen: 0,
    mouthMode: 0, // 0: Normal, 1: Grin, 2: Sad
    voiceVol: 0,
    isVoiceReady: false,
    maxL: 0.1, maxR: 0.1,
    skinThresh: 150, // UI Controlled (for removePink)
    globalScale: 0.75, // UI Controlled
    isMagenta: false // Chroma Key Toggle
};

const images = {};
let audioCtx, analyser, dataArray;

function updateState(key, val) {
    state[key] = parseFloat(val);
    console.log(`State Update: ${key} = ${val}`);
}

function toggleChroma() {
    state.isMagenta = !state.isMagenta;
    const color = state.isMagenta ? "#FF00FF" : "#050515";
    document.body.style.background = color;
    document.getElementById('stage').style.background = color;
    console.log("Chroma Key Toggle:", state.isMagenta);
}

async function initVoice() {
    try {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
        const micSource = audioCtx.createMediaStreamSource(stream);
        
        const hp = audioCtx.createBiquadFilter(); hp.type = "highpass"; hp.frequency.value = 150;
        const shelf = audioCtx.createBiquadFilter(); shelf.type = "highshelf"; shelf.frequency.value = 3000; shelf.gain.value = 5;
        
        const compressor = audioCtx.createDynamicsCompressor();
        compressor.threshold.setValueAtTime(-24, audioCtx.currentTime);
        compressor.ratio.setValueAtTime(12, audioCtx.currentTime);
        
        analyser = audioCtx.createAnalyser(); analyser.fftSize = 256;
        dataArray = new Uint8Array(analyser.frequencyBinCount);
        
        micSource.connect(hp); hp.connect(shelf); shelf.connect(analyser); shelf.connect(compressor);
        compressor.connect(audioCtx.destination); 
        
        state.isVoiceReady = true;
        document.getElementById('vStatus').innerText = "LIVE (ULTRA_STABLE)";
        document.getElementById('vStatus').style.color = "#00FF00";
        document.getElementById('startBtn').style.display = "none";
    } catch (err) {
        console.error("Voice Init Failed:", err);
        document.getElementById('vStatus').innerText = "ACCESS_DENIED";
    }
}

function drawPart(img, options = {}) {
    if (!img || !img.complete) return;
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    
    let sw = img.width / (options.isEyes ? 8 : 1);
    let sh = options.isEyes ? 120 : (options.isMouth ? 90 : img.height);
    
    let sx = options.isEyes ? (options.frame || 0) * sw : (options.isMouth ? (img.width - 300) / 2 : 0);
    let sy = options.isEyes ? 422 : (options.isMouth ? (options.frame || 0) * (img.height / 3) + 110 : 0);
    
    if (options.isMouth) {
        sw = 300;
        if (state.mouthMode === 1) sx -= 320; 
        if (state.mouthMode === 2) sx += 320;
    }

    // Apply Global Model Scale
    const gs = state.globalScale;

    ctx.save();
    ctx.translate(400 + state.curX * (options.z || 1) * gs + (options.x || 0) * gs, 
                  400 + state.curY * (options.z || 1) * gs + (options.y || 0) * gs);
    ctx.rotate(state.curRot);
    ctx.scale((options.scaleX || 1) * gs, (options.scaleY || 1) * gs);
    ctx.drawImage(img, sx, sy, sw, sh, -sw / 2, -sh / 2, sw, sh);
    ctx.restore();
}

function render() {
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 800, 800);
    
    if (state.isVoiceReady && analyser) {
        analyser.getByteFrequencyData(dataArray);
        let sum = 0; for (let i = 0; i < dataArray.length; i++) sum += dataArray[i];
        state.voiceVol = (sum / dataArray.length) / 50;
        document.getElementById('vBar').style.width = Math.min(100, (sum / dataArray.length) * 2.5) + "%";
    }
    
    drawPart(images.face, { z: 0.82, scaleX: 0.75, scaleY: 0.75 });
    
    let fL = state.eyeL > 0.4 ? 0 : 4;
    let fR = state.eyeR > 0.4 ? 0 : 4;
    drawPart(images.eyes, { x: -75, y: -45, z: 1.1, scaleX: 0.4, scaleY: 0.4, frame: fL, isEyes: true });
    drawPart(images.eyes, { x: 75, y: -45, z: 1.1, scaleX: 0.4, scaleY: 0.4, frame: fR, isEyes: true });
    
    let v = Math.max(state.mouthOpen, state.voiceVol);
    let mf = v > 0.25 ? 2 : (v > 0.08 ? 1 : 0);
    drawPart(images.mouth, { y: 112, z: 1.05, scaleX: 0.48, scaleY: mf == 2 ? 0.22 : 0.33, frame: mf, isMouth: true });
}

function animate() {
    state.curX += (state.tgtX - state.curX) * 0.1;
    state.curY += (state.tgtY - state.curY) * 0.1;
    state.curRot += (state.tgtRot - state.curRot) * 0.08;
    render();
    requestAnimationFrame(animate);
}

// removePink filter logic replacement (dynamic threshold)
async function processChromaKey(img) {
    const canvas = document.createElement('canvas');
    canvas.width = img.width; canvas.height = img.height;
    const ctx = canvas.getContext('2d'); ctx.drawImage(img, 0, 0);
    const data = ctx.getImageData(0, 0, img.width, img.height);
    const thresh = state.skinThresh;
    for (let i = 0; i < data.data.length; i += 4) {
        // Remove pink background if present (legacy support)
        if (data.data[i] > thresh && data.data[i + 2] > thresh && data.data[i + 1] < (thresh - 30)) {
            data.data[i + 3] = 0;
        }
    }
    ctx.putImageData(data, 0, 0);
    const r = new Image();
    r.src = canvas.toDataURL();
    return new Promise(res => r.onload = () => res(r));
}

window.addEventListener('keydown', (e) => {
    if (e.key === '1') state.mouthMode = 0;
    if (e.key === '2') state.mouthMode = 1;
    if (e.key === '3') state.mouthMode = 2;
});

(async function init() {
    const faceMesh = new FaceMesh({ locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}` });
    faceMesh.setOptions({ maxNumFaces: 1, refineLandmarks: true, minDetectionConfidence: 0.8, minTrackingConfidence: 0.8 });
    faceMesh.onResults((res) => {
        if (res.multiFaceLandmarks && res.multiFaceLandmarks[0]) {
            const lm = res.multiFaceLandmarks[0];
            const faceWidth = Math.sqrt(Math.pow(lm[263].x - lm[33].x, 2) + Math.pow(lm[263].y - lm[33].y, 2));
            const vL = Math.abs(lm[159].y - lm[145].y) / faceWidth;
            const vR = Math.abs(lm[386].y - lm[374].y) / faceWidth;
            state.maxL = Math.max(state.maxL || 0.1, vL);
            state.maxR = Math.max(state.maxR || 0.1, vR);
            document.getElementById('eL').innerText = vL.toFixed(3);
            document.getElementById('eR').innerText = vR.toFixed(3);
            state.eyeL = vL > (state.maxL * 0.6) ? 1 : 0;
            state.eyeR = vR > (state.maxR * 0.6) ? 1 : 0;
            state.mouthOpen = Math.abs(lm[13].y - lm[14].y) * 2.0;
            state.tgtX = (lm[1].x - 0.5) * 400; 
            state.tgtY = (lm[1].y - 0.5) * 400;
            state.tgtRot = Math.atan2(lm[152].x - lm[10].x, lm[152].y - lm[10].y) * -1;
        }
    });
    const camera = new Camera(document.getElementById('webcam'), {
        onFrame: async () => { await faceMesh.send({ image: document.getElementById('webcam') }); },
        width: 640, height: 480
    });
    camera.start();

    // Setup assets
    for (let key in b64Data) {
        images[key] = await processChromaKey(await new Promise(res => {
            let i = new Image(); i.onload = () => res(i); i.src = b64Data[key];
        }));
    }
    animate();
})();
