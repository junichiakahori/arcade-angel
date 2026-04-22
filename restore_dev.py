
import re
import base64

def restore_dev():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract assets
    asset_match = re.search(r'const embeddedAssets = (\{.*?\});', content, re.DOTALL)
    if not asset_match:
        print("Error: Could not find embeddedAssets")
        return
    assets_str = asset_match.group(1)

    # Embed Tenko Ears if not already there
    try:
        with open('assets/tenko_ears.png', 'rb') as tf:
            tenko_b64 = "data:image/png;base64," + base64.b64encode(tf.read()).decode()
    except:
        tenko_b64 = "" # Fallback

    new_html_head = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Arcade Angel - Master Puppet v0.15.123</title>
    <style>
        body { margin: 0; background: #050515; color: #00F0FF; font-family: 'Outfit', sans-serif; overflow: hidden; display: flex; height: 100vh; }
        #canvas-container { position: relative; flex: 1; display: flex; align-items: center; justify-content: center; }
        #stage { background: radial-gradient(circle, #101030 0%, #050515 100%); border: 2px solid #00F0FF; box-shadow: 0 0 50px #00F0FF22; border-radius: 12px; }
        
        .hud { position: absolute; top: 20px; left: 20px; text-shadow: 0 0 10px #00F0FF; z-index: 100; font-size: 13px; background: #101030AA; padding: 15px; border-radius: 8px; border: 1px solid #00F0FF44; pointer-events: none; backdrop-filter: blur(5px); }
        
        .settings-panel { width: 260px; height: 100vh; background: #050515EE; padding: 20px; border-left: 1px solid #0088FF44; color: #00F0FF; overflow-y: auto; scrollbar-width: thin; }
        .control-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; opacity: 0.8; font-size: 10px; font-weight: bold; letter-spacing: 1px; }
        input[type=range] { width: 100%; cursor: pointer; accent-color: #0088FF; margin-top: 5px; }
        .num-in { background: #050515; border: 1px solid #0088FF44; color: #00F0FF; width: 50px; text-align: center; border-radius: 4px; font-size: 12px; padding: 2px; }
        
        .btn { color: #00F0FF; border: 1px solid #00F0FF; padding: 10px; cursor: pointer; background: transparent; display: block; width: 100%; margin-top: 10px; font-size: 11px; text-align: center; border-radius: 4px; transition: 0.3s; font-weight: bold; }
        .btn:hover { background: #00F0FF22; box-shadow: 0 0 15px #00F0FF44; }
        .btn.active { background: #00F0FF44; border-color: #00FFFF; }
        
        .row { display: flex; align-items: center; gap: 8px; justify-content: space-between; }
        h3 { font-size: 14px; margin: 0 0 15px 0; border-bottom: 1px solid #00F0FF44; padding-bottom: 5px; color: #00FFFF; }
        
        #overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; display:flex; justify-content:center; align-items:center; cursor:pointer; }
    </style>
</head>
<body>
    <div id="overlay" onclick="this.style.display='none'; initAudio();">
        <div style="color:#00F0FF; text-align:center;">
            <h1 style="margin:0; text-shadow: 0 0 20px #00F0FF;">ARCADE ANGEL</h1>
            <p style="letter-spacing:4px;">PORTABLE PUPPET v0.15.123</p>
            <p style="font-size:12px; opacity:0.6; margin-top:20px;">[ CLICK TO INITIALIZE SYSTEM ]</p>
        </div>
    </div>

    <div id="canvas-container">
        <div class="hud" id="hud_display">BOOTING...</div>
        <canvas id="stage" width="800" height="800"></canvas>
    </div>

    <div class="settings-panel">
        <h3>SYSTEM SETTINGS</h3>
        <div class="control-group"><label>GLOBAL SCALE</label><div class="row"><input type="range" id="scale" min="0.1" max="1.5" step="0.01" value="0.5"><input type="number" id="scale_num" class="num-in"></div></div>
        <div class="control-group"><label>PIVOT Y (Rotation Center)</label><div class="row"><input type="range" id="pivotY" min="0" max="800" value="600"><input type="number" id="pivotY_num" class="num-in"></div></div>
        
        <h3>FACIAL GEOMETRY</h3>
        <div class="control-group"><label>EYE POS Y</label><div class="row"><input type="range" id="eyeY" min="-200" max="200" value="-79"><input type="number" id="eyeY_num" class="num-in"></div></div>
        <div class="control-group"><label>EYE DISTANCE</label><div class="row"><input type="range" id="eyeX" min="30" max="250" value="112"><input type="number" id="eyeX_num" class="num-in"></div></div>
        <div class="control-group"><label>MOUTH POS Y</label><div class="row"><input type="range" id="mouthY" min="-100" max="300" value="123"><input type="number" id="mouthY_num" class="num-in"></div></div>
        
        <h3>PHYSICS & SENSITIVITY</h3>
        <div class="control-group"><label>SMILE SENSITIVITY</label><div class="row"><input type="range" id="smileSens" min="30" max="100" value="60"><input type="number" id="smileSens_num" class="num-in"></div></div>
        <div class="control-group"><label style="color:#FF00FF">HAIR PHYSICS (LAG)</label><div class="row"><input type="range" id="hairLag" min="0" max="1" step="0.01" value="0.5"><input type="number" id="hairLag_num" class="num-in"></div></div>
        
        <h3>VOCAL MAPPING</h3>
        <div class="control-group"><label>THRES A (Open)</label><div class="row"><input type="range" id="thresA" min="0" max="100" value="30"><input type="number" id="thresA_num" class="num-in"></div></div>
        <div class="control-group"><label>THRES U (Narrow)</label><div class="row"><input type="range" id="thresU" min="0" max="100" value="2"><input type="number" id="thresU_num" class="num-in"></div></div>
        
        <div class="btn" id="smileToggle" onclick="toggleSmile()">MODE: NORMAL</div>
        <div class="btn" id="tenkoToggle" onclick="toggleTenko()">EARS: OFF</div>
        
        <div class="control-group" style="margin-top:10px">
            <label>COSTUME SELECT</label>
            <select id="costumeSelect" onchange="state.costume = this.value" style="width:100%; height:30px; background:#111; color:#00F0FF; border:1px solid #00F0FF44;">
                <option value="cyber">Cybernetic Suit</option>
                <option value="gothic">Gothic Lolita</option>
                <option value="none">Face Only (Static)</option>
            </select>
        </div>
        
        <div class="btn" style="border-color: #FF4444; color: #FF4444" onclick="resetState()">EMERGENCY RESET</div>
    </div>

    <video id="webcam" autoplay playsinline style="display:none"></video>

    <!-- Portable Dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>

    <script>
    """

    new_script_body = f"""
        const embeddedAssets = {assets_str};
        embeddedAssets['tenko_ears'] = "{tenko_b64}";

        const state = {{
            curX: 0, curY: 0, curRot: 0, tgtX: 0, tgtY: 0, tgtRot: 0,
            eyeL: 1, eyeR: 1, mouthOpen: 0, voiceVol: 0,
            eyeX: 112, eyeY: -79, eyeSize: 0.76, mouthY: 123, globalScale: 0.5,
            isHappy: false, isTenko: false, costume: 'cyber',
            thresA: 30, thresU: 2, thresI: 14,
            pivotY: 600, smileSens: 60, detectedVowel: "---",
            breath: 0, breathSpeed: 0.04, breathScale: 1.0,
            hairLag: 0.6, hairRotL: 0, hairRotR: 0,
            isAudioReady: false
        }};

        const images = {{}};
        let audioCtx, analyser, dataArray;

        window.resetState = function() {{
            Object.assign(state, {{
                globalScale: 0.5, pivotY: 600, eyeX: 112, eyeY: -79, mouthY: 123,
                smileSens: 60, hairLag: 0.6, thresA: 30, thresU: 2
            }});
            syncUI();
        }};

        function syncUI() {{
            ['scale','pivotY','eyeX','eyeY','mouthY','smileSens','hairLag','thresA','thresU'].forEach(id => {{
                const el = document.getElementById(id); if(el) el.value = state[id];
                const nm = document.getElementById(id + '_num'); if(nm) nm.value = state[id];
            }});
        }}

        function toggleSmile() {{ state.isHappy = !state.isHappy; document.getElementById('smileToggle').innerText = state.isHappy ? "MODE: SMILE" : "MODE: NORMAL"; }}
        function toggleTenko() {{ state.isTenko = !state.isTenko; document.getElementById('tenkoToggle').innerText = state.isTenko ? "EARS: ON" : "EARS: OFF"; }}

        async function initAudio() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioCtx.createMediaStreamSource(stream);
                analyser = audioCtx.createAnalyser(); analyser.fftSize = 256;
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                source.connect(analyser); state.isAudioReady = true;
            }} catch(e) {{ console.warn("Audio Context init failed:", e); }}
        }}

        function drawLayer(img, options = {{}}) {{
            if (!img) return;
            const ctx = document.getElementById('stage').getContext('2d');
            const gs = state.globalScale;
            let sw = img.width, sh = img.height, sx = 0, sy = 0;
            
            if (options.isEyes) {{ sw = 210; sh = 165; sx = (options.frame % 4) * 256 + 23; sy = Math.floor(options.frame / 4) * 256 + 45; }}
            else if (options.isMouth) {{ sw = 210; sh = 120; sx = (options.frame % 3) * (img.width/3) + (img.width/3-sw)/2; sy = Math.floor(options.frame/3)*(img.height/3)+(img.height/3-sh)/2; }}

            ctx.save();
            let pY = state.pivotY;
            let hX = state.curX * gs * 0.2, hY = state.curY * gs * 0.1;
            let breathOff = Math.sin(state.breath) * 6 * state.breathScale;
            
            ctx.translate(400 + hX, 400 + hY + pY * gs + breathOff); 
            ctx.rotate(options.rot || state.curRot);
            ctx.translate((options.x || 0) * gs, ((options.y || 0) - pY) * gs);
            ctx.scale((options.scaleX || 1) * gs * (options.flip ? -1 : 1), (options.scaleY || 1) * gs);
            
            if (options.clipX) {{
                // PHYSICS SPLIT CLIP
                ctx.drawImage(img, options.clipX, 0, options.clipW, img.height, options.offX || -img.width/2, -img.height/2, options.clipW, img.height);
            }} else {{
                ctx.drawImage(img, sx, sy, sw, sh, -sw/2, -sh/2, sw, sh);
            }}
            ctx.restore();
        }}

        async function init() {{
            try {{
                const fm = new FaceMesh({{ locateFile: (f) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{f}}` }});
                fm.setOptions({{ maxNumFaces: 1, refineLandmarks: true, minDetectionConfidence: 0.8, minTrackingConfidence: 0.8 }});
                fm.onResults((res) => {{
                    if (res.multiFaceLandmarks && res.multiFaceLandmarks.length > 0) {{
                        const lm = res.multiFaceLandmarks[0];
                        state.eyeL = Math.max(0, Math.min(1, (Math.abs(lm[159].y - lm[145].y) / Math.abs(lm[33].x - lm[133].x)) * 5));
                        state.eyeR = Math.max(0, Math.min(1, (Math.abs(lm[386].y - lm[374].y) / Math.abs(lm[263].x - lm[362].x)) * 5));
                        state.mouthOpen = (Math.abs(lm[13].y - lm[14].y) / Math.abs(lm[78].x - lm[308].x)) * 100;
                        state.tgtX = (lm[1].x - 0.5) * 400; 
                        state.tgtY = (lm[1].y - 0.4) * 400;
                        state.tgtRot = Math.atan2(lm[152].y - lm[10].y, lm[152].x - lm[10].x) - Math.PI/2;
                    }}
                }});

                const video = document.getElementById('webcam');
                const cam = new Camera(video, {{ onFrame: async () => {{ await fm.send({{ image: video }}); }}, width: 640, height: 480 }});
                cam.start();

                for (let k in embeddedAssets) {{
                    const i = new Image(); i.src = embeddedAssets[k];
                    await new Promise(r => i.onload = r);
                    images[k] = i;
                }}

                ['scale','pivotY','eyeX','eyeY','mouthY','smileSens','hairLag','thresA','thresU'].forEach(id => {{
                    const el = document.getElementById(id); const nm = document.getElementById(id + '_num');
                    const sync = (v) => {{ state[id] = parseFloat(v); if(el) el.value = v; if(nm) nm.value = v; }};
                    if(el) el.oninput = (e) => sync(e.target.value);
                    if(nm) nm.oninput = (e) => sync(e.target.value);
                }});

                requestAnimationFrame(function animate() {{
                    const canvas = document.getElementById('stage'); if(!canvas) return;
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0,0,800,800);
                    
                    state.curX += (state.tgtX - state.curX) * 0.12;
                    state.curY += (state.tgtY - state.curY) * 0.12;
                    state.curRot += (state.tgtRot - state.curRot) * 0.12;
                    state.breath += state.breathSpeed;

                    // Hair Physics Damping
                    let lagFactor = 1.0 - state.hairLag * 0.5;
                    state.hairRotL += (state.curRot - state.hairRotL) * lagFactor;
                    state.hairRotR += (state.curRot - state.hairRotR) * (lagFactor * 0.9);

                    if (state.isAudioReady && analyser) {{
                        analyser.getByteFrequencyData(dataArray);
                        let sum = 0; for (let r = 0; r < dataArray.length; r++) sum += dataArray[r];
                        state.voiceVol = (sum / dataArray.length);
                    }}

                    const gs = state.globalScale;
                    
                    // 1. Draw Body
                    let bodyImg = state.costume === 'cyber' ? images.body_cyber : (state.costume === 'gothic' ? images.body_gothic : null);
                    if(bodyImg) {{
                        ctx.save();
                        ctx.translate(400 + state.curX * gs * 0.05, 400 + state.curY * gs * 0.05 + 300 * gs + Math.sin(state.breath)*3*gs);
                        ctx.scale(gs, gs);
                        ctx.drawImage(bodyImg, -bodyImg.width/2, -bodyImg.height/2);
                        ctx.restore();
                    }}

                    // 2. Draw Ears (if Tenko)
                    if(state.isTenko && images.tenko_ears) {{
                        drawLayer(images.tenko_ears, {{ y: -150, scaleX: 0.8, scaleY: 0.8 }});
                    }}

                    // 3. Draw Face with HAIR PHYSICS CLIPPING
                    if(images.face) {{
                        let fw = images.face.width, fh = images.face.height;
                        let slice = fw * 0.25;
                        // Left Twintail (Physics Lag)
                        drawLayer(images.face, {{ clipX: 0, clipW: slice, rot: state.hairRotL, offX: -fw/2 }});
                        // Middle Head (Face)
                        drawLayer(images.face, {{ clipX: slice, clipW: fw - slice*2, rot: state.curRot, offX: -fw/2 + slice }});
                        // Right Twintail (Physics Lag)
                        drawLayer(images.face, {{ clipX: fw - slice, clipW: slice, rot: state.hairRotR, offX: -fw/2 + fw - slice }});
                    }}

                    // 4. Draw Eyes & Mouth
                    const getEyeFrame = (o) => (state.isHappy ? (o > 0.3 ? 4 : o > 0.1 ? 6 : 15) : (o > 0.3 ? 0 : o > 0.1 ? 2 : 15));
                    drawLayer(images.eyeUni, {{ x: -state.eyeX, y: state.eyeY, scaleX: state.eyeSize, scaleY: state.eyeSize, frame: getEyeFrame(state.eyeR), isEyes: true, flip: true }});
                    drawLayer(images.eyeUni, {{ x: state.eyeX, y: state.eyeY, scaleX: state.eyeSize, scaleY: state.eyeSize, frame: getEyeFrame(state.eyeL), isEyes: true, flip: false }});

                    let v = Math.max(state.mouthOpen, state.voiceVol);
                    let mf = 0;
                    if (v >= state.thresA) {{ mf = 7; state.detectedVowel = "A"; }}
                    else if (v >= state.thresI) {{ mf = 4; state.detectedVowel = "I"; }}
                    else if (v >= state.thresU) {{ mf = 6; state.detectedVowel = "U"; }}
                    else {{ mf = state.isHappy ? 3 : 0; state.detectedVowel = "CLOSED"; }}
                    drawLayer(images.mouthUni, {{ y: state.mouthY, scaleX: 0.45, scaleY: 0.45, frame: mf, isMouth: true }});

                    const hud = document.getElementById("hud_display");
                    if(hud) hud.innerHTML = `ARCADE_ANGEL v0.15.123<br>DET: ${{state.detectedVowel}} | VOL: ${{state.voiceVol.toFixed(1)}}`;

                    requestAnimationFrame(animate);
                }});
            }} catch (e) {{ console.error("BOOT FAILURE:", e); }}
        }}
        init();
    </script>
</body>
</html>
"""

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(new_html_head + new_script_body)

if __name__ == '__main__':
    restore_dev()
