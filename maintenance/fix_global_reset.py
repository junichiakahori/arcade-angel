import re

def absolute_sync_fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. DEFINE GLOBAL resetState FUNCTION
    # This will handle the onclick="resetState()" from the HTML
    reset_state_func = """
        window.resetState = function() {
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
            
            const syncId = (id, val) => { const el = document.getElementById(id); if(el) el.value = val; };
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
    """

    # 2. FIX addEventListener NULL ERRORS (Safety check wrapper)
    # We will wrap the slider setup in a safe loop
    content = content.replace(
        "document.getElementById('scale').addEventListener", 
        "if(document.getElementById('scale')) document.getElementById('scale').addEventListener"
    )
    # Perform similar safety for common ones or wrap correctly
    
    # Clean up previous turn's reset listener to avoid duplicates or conflicts
    content = re.sub(r"document\.getElementById\('reset-defaults'\)\.addEventListener\('click', .*?\}\);", "", content, flags=re.DOTALL)
    
    # Inject the new global function before init()
    if 'window.resetState' not in content:
        content = content.replace('async function init() {', reset_state_func + '\n        async function init() {')

    # 3. Bump version to v0.15.116
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113|114|115)', 'v0.15.116', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    absolute_sync_fix()
