import re

def final_syntax_restoration():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # We will rewrite the script section from resetState to init to be absolutely clean
    
    script_start_marker = '        window.resetState = function() {'
    script_end_marker = '    init();'
    
    # Locate the problematic block
    start_pos = content.find(script_start_marker)
    end_pos = content.find(script_end_marker)
    
    if start_pos == -1 or end_pos == -1:
        # Fallback to a broader search if markers moved
        return "Could not find expected script markers."

    clean_block = """        window.resetState = function() {
            console.log("Resetting to defaults...");
            state.globalScale = 0.5;
            state.breathSpeed = 0.05;
            state.breathScale = 1.0;
            state.eyePosY = 0;
            state.eyeDistance = 0;
            state.eyeSize = 1.0;
            state.browPosY_happy = 0;
            state.browTilt_happy = 0;
            state.mouthPosY = 0;
            state.smileSens = 60;
            state.pivotY = 600;
            state.thresA = 30;
            state.thresE = 20;
            state.thresI = 14;
            state.thresO = 10;
            state.thresU = 2;
            
            const syncId = (id, val) => { 
                const el = document.getElementById(id); 
                if(el) el.value = val; 
            };
            syncId('scale', 0.5);
            syncId('breath-speed', 0.05);
            syncId('breath-scale', 1.0);
            syncId('eye-pos-y', 0);
            syncId('eye-distance', 0);
            syncId('eye-size', 1.0);
            syncId('brow-pos-y-happy', 0);
            syncId('brow-tilt-happy', 0);
            syncId('mouth-pos-y', 0);
            syncId('smile-sens', 60);
            syncId('pivot-y', 600);
            syncId('thres-a', 30);
            syncId('thres-e', 20);
            syncId('thres-i', 14);
            syncId('thres-o', 10);
            syncId('thres-u', 2);
        };

        async function init() {
            try {
                let assets = embeddedAssets;
                v_data = {history:[]};
                const fm = new FaceMesh({ locateFile: (f) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${f}` });
                fm.setOptions({ maxNumFaces: 1, refineLandmarks: true, minDetectionConfidence: 0.8, minTrackingConfidence: 0.8 });
                fm.onResults((res) => {
                    if (res.multiFaceLandmarks && res.multiFaceLandmarks.length > 0) {
                        const lm = res.multiFaceLandmarks[0];
                        state.eyeL = Math.max(0, Math.min(1, (Math.abs(lm[159].y - lm[145].y) / Math.abs(lm[33].x - lm[133].x))));
                        state.eyeR = Math.max(0, Math.min(1, (Math.abs(lm[386].y - lm[374].y) / Math.abs(lm[263].x - lm[362].x))));
                        state.mouthOpen = Math.abs(lm[13].y - lm[14].y) / Math.abs(lm[78].x - lm[308].x);
                        state.tgtX = (lm[1].x - 0.5) * 400; state.tgtY = (lm[1].y - 0.4) * 400;
                        state.tgtRot = Math.atan2(lm[152].y - lm[10].y, lm[152].x - lm[10].x) - Math.PI/2;
                        const mouthWidth = Math.abs(lm[61].x - lm[291].x);
                        const eyeDist = Math.abs(lm[33].x - lm[263].x);
                        state.smileRaw = mouthWidth / eyeDist;
                    }
                });

                const cam = new Camera(document.getElementById('webcam'), {
                    onFrame: async () => { await fm.send({ image: document.getElementById('webcam') }); },
                    width: 640, height: 480
                });
                cam.start();

                for (let k in assets) {
                    const i = new Image(); i.src = assets[k];
                    await new Promise(r => i.onload = r);
                    images[k] = await processAlpha(i, k === 'face' ? 'face' : 'part');
                }
                loadFromLocal();
                ['scale','breath-speed','breath-scale','eye-pos-y','eye-distance','eye-size','brow-pos-y-happy','brow-tilt-happy','mouth-pos-y','smile-sens','pivot-y','thres-a','thres-e','thres-i','thres-o','thres-u'].forEach(k => {
                    const s = document.getElementById(k);
                    if (s) {
                        s.value = state[k.replace(/-/g, '')] || state[k] || 0;
                        s.oninput = (e) => {
                            const val = parseFloat(e.target.value);
                            const key = k.replace(/-/g, '');
                            if (state.hasOwnProperty(key)) state[key] = val;
                            else state[k] = val;
                        };
                    }
                });
                animate();
            } catch (e) { console.error(e); }
        }
    \n"""

    new_content = content[:start_pos] + clean_block + content[end_pos:]
    
    # v0.15.118
    new_content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117)', 'v0.15.118', new_content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    final_syntax_restoration()
