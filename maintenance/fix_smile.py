import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the calculation in onResults (remove redundant / 100)
    content = content.replace('(state.smileRaw - (state.smileSens/100)) / 0.2', '(state.smileRaw - state.smileSens) / 0.2')

    # 2. Fix the HUD display (remove redundant / 100) using a more precise regex to avoid shell issues
    content = content.replace('SENS:${(state.smileSens/100).toFixed(2)}', 'SENS:${state.smileSens.toFixed(2)}')

    # Update version
    content = content.replace('v0.15.96', 'v0.15.97')
    content = content.replace('2026-04-18 06:30:00', '2026-04-18 06:35:00')

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
