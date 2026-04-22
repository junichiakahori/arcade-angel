import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Correct the function name
    content = content.replace('initAudio();', 'initVoice();')

    # Fix locateFile with safe string formatting
    face_mesh_lib = "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh"
    locate_file_code = "locateFile: (file) => `" + face_mesh_lib + "/${file}`"
    
    # Try to insert or replace locateFile
    if 'locateFile' in content:
        content = re.sub(r'locateFile\s*:\s*\(file\)\s*=>\s*`.*?`', locate_file_code, content)
    else:
        content = content.replace('new FaceMesh({', 'new FaceMesh({' + locate_file_code + ', ')

    # Version and Time
    content = re.sub(r'v0\.15\.102', 'v0.15.103', content)
    content = re.sub(r'2026-04-18 07:00:00', '2026-04-18 07:10:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
