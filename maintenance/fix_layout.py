import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    hud_html = "<div class=\"hud\">${state.foxMode ? 'DIVINE: TENKO (天狐)' : 'UNIT: ARCADE_ANGEL' } v0.15.95 (2026-04-18 06:25:00)</div>"

    panel_content = """
        <div class="control-group"><label>EYE POS Y</label><input type="range" id="eyeY" min="-300" max="100" value="-79" oninput="updateState('eyeY', this.value)"></div>
        <div class="control-group"><label>EYE DISTANCE</label><input type="range" id="eyeX" min="30" max="250" value="112" oninput="updateState('eyeX', this.value)"></div>
        <div class="control-group"><label>EYE SIZE</label><input type="range" id="eyeSize" min="0.3" max="1.5" step="0.01" value="0.76" oninput="updateState('eyeSize', this.value)"></div>
        
        <div class="control-group"><label style="color:#00FF88">BROW POS Y (Happy)</label><div class="row"><input type="range" id="browY" min="-50" max="50" value="5" oninput="syncUI('browY', this.value)"><input type="number" id="browY_num" class="num-in" oninput="syncUI('browY', this.value)"></div></div>
        <div class="control-group"><label style="color:#00FF88">BROW TILT (Happy)</label><div class="row"><input type="range" id="browTilt" min="-0.5" max="0.5" step="0.01" value="0" oninput="syncUI('browTilt', this.value)"><input type="number" id="browTilt_num" class="num-in" oninput="syncUI('browTilt', this.value)"></div></div>
            
        <div class="control-group"><label style="color:#00AAFF">BREATH SPEED</label><div class="row"><input type="range" id="breathSpeed" min="0" max="3" step="0.1" value="1.0" oninput="syncUI('breathSpeed', this.value)"></div></div>
        <div class="control-group"><label style="color:#00AAFF">BREATH SCALE</label><div class="row"><input type="range" id="breathScale" min="0" max="5" step="0.1" value="1.0" oninput="syncUI('breathScale', this.value)"></div></div>
        <div class="control-group"><label>MOUTH POS Y</label><input type="range" id="mouthY" min="0" max="300" value="123" oninput="updateState('mouthY', this.value)"></div>
        <div class="control-group"><label style="color:#FFAA00">SMILE SENS (Auto-Happy)</label><div class="row"><input type="range" id="smileSens" min="30" max="90" value="58" oninput="syncUI('smileSens', this.value)"><input type="number" id="smileSens_num" class="num-in" oninput="syncUI('smileSens', this.value)"></div></div>
        <div class="control-group"><label style="color:#00FF88">ROT PIVOT Y (Depth)</label><div class="row"><input type="range" id="pivotY" min="0" max="600" value="600" oninput="syncUI('pivotY', this.value)"><input type="number" id="pivotY_num" class="num-in" oninput="syncUI('pivotY', this.value)"></div></div>
        <div class="control-group"><label style="color:#FF00FF">THRES A (Wide)</label><div class="row"><input type="range" id="thresA" min="0" max="80" value="27" oninput="syncUI('thresA', this.value)"><input type="number" id="thresA_num" class="num-in" oninput="syncUI('thresA', this.value)"></div></div>
        <div class="control-group"><label style="color:#FF00FF">THRES E (Mid)</label><div class="row"><input type="range" id="thresE" min="0" max="80" value="18" oninput="syncUI('thresE', this.value)"><input type="number" id="thresE_num" class="num-in" oninput="syncUI('thresE', this.value)"></div></div>
        <div class="control-group"><label style="color:#FF00FF">THRES I (Narrow)</label><div class="row"><input type="range" id="thresI" min="0" max="80" value="14" oninput="syncUI('thresI', this.value)"><input type="number" id="thresI_num" class="num-in" oninput="syncUI('thresI', this.value)"></div></div>
        <div class="control-group"><label style="color:#FF00FF">THRES O (Med-Round)</label><div class="row"><input type="range" id="thresO" min="0" max="80" value="5" oninput="syncUI('thresO', this.value)"><input type="number" id="thresO_num" class="num-in" oninput="syncUI('thresO', this.value)"></div></div>
        <div class="control-group"><label style="color:#FF00FF">THRES U (Small-Round)</label><div class="row"><input type="range" id="thresU" min="0" max="80" value="11" oninput="syncUI('thresU', this.value)"><input type="number" id="thresU_num" class="num-in" oninput="syncUI('thresU', this.value)"></div></div>
        <div id="smileBtn" class="btn" onclick="toggleSmile()">MODE: SMILE</div>
        <div class="row">
            <div class="btn" onclick="exportProfile()">EXPORT</div>
            <div class="btn" onclick="importProfile()">IMPORT</div>
        </div>
        <div class="btn" style="border-color: #FF5555; color: #FF5555" onclick="resetState()">RESET DEFAULTS</div>
        <div class="dev-only">
            <div id="tenkoBtn" class="btn" style="border-color: #FFD700; color: #FFD700" onclick="toggleFoxMode()">TENKO MODE: OFF</div>
            <div class="btn" onclick="setCostume('none')">COSTUME: NONE</div>
            <div class="btn" onclick="setCostume('cyber')">COSTUME: CYBER</div>
            <div class="btn" onclick="setCostume('gothic')">COSTUME: GOTHIC</div>
            <div id="greetBtn" class="btn" style="background:#00FF8833;" onclick="greet()">GREETING (OHAYOU)</div>
            <div id="startBtn" class="btn" onclick="initVoice()">ENABLE VOICE</div>
        </div>
        <div class="btn" style="background: #ffffff11; color: #888; font-size: 10px" onclick="switchVersion()">SWITCH VERSION (To Stable)</div>
    """

    new_body = "\n<body>\n    <script>\n        const isDev = window.location.pathname.includes('dev.html');\n        if (isDev) { document.write('<style>.dev-only { display: block; }</style>'); }\n    </script>\n    " + hud_html + "\n\n    <div class=\"settings-panel\">\n" + panel_content.strip() + "\n    </div>\n\n    <canvas id=\"stage\" width=\"800\" height=\"800\"></canvas>\n    <video id=\"webcam\" autoplay playsinline style=\"display:none\"></video>\n"

    pattern = re.compile(r'<body>.*?<script src="https', re.DOTALL)
    content = pattern.sub(new_body + "\n\n    <script src=\"https", content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
