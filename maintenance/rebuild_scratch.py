import re

def rebuild_from_scratch():
    with open('dev.html', 'r', encoding='utf-8') as f:
        full_content = f.read()

    # 1. EXTRACT ASSETS EARLIER (Take it from the most recent or any embeddedAssets block)
    # We'll try to find a valid JSON-like block for embeddedAssets
    asset_match = re.search(r'const embeddedAssets = (\{.*?\});', full_content, re.DOTALL)
    if not asset_match:
        return "FATAL: Could not find embeddedAssets"
    
    # Pre-process the assets to be clean (remove plus signs and quotes if they were added during split)
    asset_json_str = asset_match.group(1)
    # Clean up the splitted string artifacts if any to get raw data
    asset_json_str = re.sub(r'["\']\s*\+\s*\n\s*["\']', '', asset_json_str)

    # 2. DEFINE THE CLEAN TEMPLATE
    head_part = full_content.split('<script>')[0] + '<script>\n'
    tail_part = '\n    </script>\n' + full_content.split('</script>')[-1]

    clean_script_body = """
        const embeddedAssets = """ + asset_json_str + """;

        const state = {
            curX: 0, curY: 0, curRot: 0, tgtX: 0, tgtY: 0, tgtRot: 0,
            eyeL: 1, eyeR: 1, mouthOpen: 0, voiceVol: 0,
            eyeX: 112, eyeY: -79, eyeSize: 0.76, mouthY: 123, globalScale: 0.5,
            isHappy: false, skinTone: 0, costume: 'none', isVoiceReady: false,
            thresA: 30, thresE: 20, thresI: 14, thresO: 10, thresU: 2,
            pivotY: 600, smileSens: 60, smileDegree: 0, breathSpeed: 0.05, breathScale: 1.0,
            eyeDistance: 0, browPosY_happy: 0, browTilt_happy: 0, mouthPosY: 0, smileRaw: 0
        };

        const images = {};
        const v_data = {history:[]};

        window.resetState = function() {
            console.log("Resetting...");
            Object.assign(state, {
                globalScale: 0.5, breathSpeed: 0.05, breathScale: 1.0,
                eyePosY: 0, eyeDistance: 0, eyeSize: 1.0, 
                browPosY_happy: 0, browTilt_happy: 0, mouthPosY: 0,
                smileSens: 60, pivotY: 600, thresA: 30, thresE: 20, thresI: 14, thresO: 10, thresU: 2
            });
            ['scale','breath-speed','breath-scale','eye-pos-y','eye-distance','eye-size','brow-pos-y-happy','brow-tilt-happy','mouth-pos-y','smile-sens','pivot-y','thres-a','thres-e','thres-i','thres-o','thres-u'].forEach(id => {
                const el = document.getElementById(id);
                if(el) {
                    const key = id.replace(/-/g, '');
                    el.value = state[key] || state[id] || 0;
                }
            });
        };

        async function processAlpha(img, mode) {
            const canvas = document.createElement('canvas');
            canvas.width = img.width; canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            return canvas; // Simplified alpha for performance stability
        }

        async function init() {
            try {
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
                        state.smileRaw = Math.abs(lm[61].x - lm[291].x) / Math.abs(lm[33].x - lm[263].x);
                    }
                });

                const video = document.getElementById('webcam');
                const cam = new Camera(video, {
                    onFrame: async () => { await fm.send({ image: video }); },
                    width: 640, height: 480
                });
                cam.start();

                for (let k in embeddedAssets) {
                    const i = new Image(); i.src = embeddedAssets[k];
                    await new Promise(r => i.onload = r);
                    images[k] = i;
                }
                
                ['scale','breath-speed','breath-scale','eye-pos-y','eye-distance','eye-size','brow-pos-y-happy','brow-tilt-happy','mouth-pos-y','smile-sens','pivot-y','thres-a','thres-e','thres-i','thres-o','thres-u'].forEach(id => {
                    const el = document.getElementById(id);
                    if(el) {
                        el.oninput = (e) => {
                            const val = parseFloat(e.target.value);
                            const key = id.replace(/-/g, '');
                            if (state.hasOwnProperty(key)) state[key] = val;
                            else state[id] = val;
                        };
                    }
                });

                requestAnimationFrame(function animate() {
                    const stage = document.getElementById('stage');
                    if(!stage) return;
                    const ctx = stage.getContext('2d');
                    ctx.clearRect(0,0,800,800);
                    
                    const hud = document.getElementById("hud_display");
                    if(hud) hud.innerText = `UNIT: ARCADE_ANGEL v0.15.120 | PORTABLE`;

                    ctx.save();
                    ctx.translate(400, state.pivotY);
                    ctx.scale(state.globalScale, state.globalScale);
                    
                    // Basic render (body, then face)
                    if(images.body) ctx.drawImage(images.body, -images.body.width/2, -images.body.height/2);
                    if(images.face) ctx.drawImage(images.face, -images.face.width/2, -images.face.height/2);
                    
                    ctx.restore();
                    requestAnimationFrame(animate);
                });

            } catch (e) { console.error("Init failed:", e); }
        }

        init();
    """

    final_html = head_part + clean_script_body + tail_part
    
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == '__main__':
    rebuild_from_scratch()
