import re

def fix_reset_button():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Redefine the reset defaults logic
    # We will look for the button event listener and inject a robust reset function
    
    reset_logic = """
        document.getElementById('reset-defaults').addEventListener('click', () => {
            // Reset state to original defaults
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
            state.thresU = 2; // Updated default
            
            // Sync all UI sliders
            document.getElementById('scale').value = state.globalScale;
            document.getElementById('breath-speed').value = state.breathSpeed;
            document.getElementById('breath-scale').value = state.breathScale;
            document.getElementById('eye-pos-y').value = state.eyePosY;
            document.getElementById('eye-distance').value = state.eyeDistance;
            document.getElementById('eye-size').value = state.eyeSize;
            document.getElementById('brow-pos-y-happy').value = state.browPosY_happy;
            document.getElementById('brow-tilt-happy').value = state.browTilt_happy;
            document.getElementById('mouth-pos-y').value = state.mouthPosY;
            document.getElementById('smile-sens').value = state.smileSens;
            document.getElementById('pivot-y').value = state.pivotY;
            document.getElementById('thres-a').value = state.thresA;
            document.getElementById('thres-e').value = state.thresE;
            document.getElementById('thres-i').value = state.thresI;
            document.getElementById('thres-o').value = state.thresO;
            document.getElementById('thres-u').value = state.thresU;
            
            console.log("Defaults Reset.");
        });
    """

    # If the button listener already exists, replace it, otherwise append to init or script end
    if "document.getElementById('reset-defaults')" in content:
        # Replace existing one (surgical regex)
        content = re.sub(r"document\.getElementById\('reset-defaults'\)\.addEventListener\('click', .*?\}\);", reset_logic, content, flags=re.DOTALL)
    else:
        # Append before closing script
        content = content.replace('    init();', reset_logic + '\n    init();')

    # 2. Bump version to v0.15.115
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113|114)', 'v0.15.115', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_reset_button()
