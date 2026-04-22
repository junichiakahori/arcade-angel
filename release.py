
import os
import shutil
import json
import subprocess
import webbrowser
from datetime import datetime

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True

def release():
    # 1. Load version info
    with open('version_history_dev.json', 'r', encoding='utf-8') as f:
        dev_history = json.load(f)
    
    current_version = dev_history['current_version']
    print(f"🚀 Releasing {current_version}...")

    # 2. Backup current index.html
    if os.path.exists('index.html'):
        # Get version of old index.html (rough check)
        backup_name = f"index_backup_last.html"
        shutil.copy('index.html', backup_name)
        print(f"📦 Backed up current index.html to {backup_name}")

    # 3. Copy dev.html to index.html
    shutil.copy('dev.html', 'index.html')
    print(f"✅ Synced dev.html to index.html")

    # 4. Update version_history.json
    with open('version_history.json', 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    # Check if this version is already in history
    if not any(h['version'] == current_version for h in history['history']):
        new_entry = {
            "version": current_version,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%00"),
            "notes": f"STABLE DEPLOYMENT ({current_version}): Synchronized with latest dev features."
        }
        history['history'].insert(0, new_entry)
        history['current_version'] = current_version
        history['last_updated'] = new_entry['date']
        
        with open('version_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"📝 Updated version_history.json to {current_version}")

    # 5. Update README.md badge
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        
        import re
        new_readme = re.sub(r'Version-v[0-9.]+', f'Version-{current_version}', readme)
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_readme)
        print(f"🏷️ Updated README.md badge")

    # 6. Git Push
    print("📤 Pushing to GitHub...")
    if run_cmd("git add index.html version_history.json README.md index_backup_last.html"):
        if run_cmd(f'git commit -m "Auto-Release {current_version}"'):
            run_cmd("git push origin main")
            print("🚀 Pushed to GitHub successfully!")

    # 7. Open Browser
    print("🌐 Opening local environment...")
    webbrowser.open("http://localhost:8000/")

if __name__ == "__main__":
    release()
