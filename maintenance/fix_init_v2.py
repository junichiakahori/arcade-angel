import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FIX THE TYPO: initAudio -> initVoice
    content = content.replace('initAudio()', 'initVoice()')

    # 2. ENSURE LOCATEFILE IS CORRECTLY INJECTED
    # First, remove existing FaceMesh initialization to avoid duplicates or mess
    content = re.sub(r'const fm = new FaceMesh\(.*?\);', 'const fm = new FaceMesh({ locateFile: (f) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${f}` });', content)

    # 3. Update version and timestamp
    content = re.sub(r'v0\.15\.(101|102)', 'v0.15.103', content)
    content = re.sub(r'2026-04-18 07:00:00', '2026-04-18 07:15:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
