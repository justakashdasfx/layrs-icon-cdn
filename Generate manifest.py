"""
generate_manifest.py
--------------------
Scans your icons folder and generates icons.json.
Also prints instructions for pasting into code.js.

Run from the ROOT of your layrs-icon-cdn repo:
    python generate_manifest.py
"""

import os
import json

ICONS_DIR = None
OUTPUT_FILE = "icons.json"

def find_icons_dir():
    for name in ["icons", "Icons", "ICONS"]:
        if os.path.exists(name):
            return name
    return None

def generate():
    global ICONS_DIR
    ICONS_DIR = find_icons_dir()

    if not ICONS_DIR:
        print(f"❌  No icons folder found.")
        print(f"   Current dir: {os.getcwd()}")
        return

    print(f"📁  Scanning: {ICONS_DIR}/\n")
    libraries = {}

    for library in sorted(os.listdir(ICONS_DIR)):
        lib_path = os.path.join(ICONS_DIR, library)
        if not os.path.isdir(lib_path) or library.startswith('.'):
            continue

        libraries[library] = {}
        print(f"📦  {library}")

        for category in sorted(os.listdir(lib_path)):
            cat_path = os.path.join(lib_path, category)
            if not os.path.isdir(cat_path) or category.startswith('.'):
                continue

            icons = []
            for root, dirs, files in os.walk(cat_path):
                dirs[:] = [d for d in sorted(dirs) if not d.startswith('.')]
                for filename in sorted(files):
                    if filename.endswith('.svg') and not filename.startswith('.'):
                        icons.append(filename[:-4])

            icons = sorted(list(dict.fromkeys(icons)))
            libraries[library][category] = icons
            print(f"   ✓ {category}: {len(icons)} icons")

    manifest = { "version": "1.0.0", "libraries": libraries }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    total = sum(len(v) for lib in libraries.values() for v in lib.values())
    print(f"\n✅  {OUTPUT_FILE} saved — {total} icons total")
    print(f"\n{'─'*50}")
    print(f"📋  NEXT STEP:")
    print(f"   1. Open icons.json")
    print(f"   2. Copy all the contents (Ctrl+A, Ctrl+C)")
    print(f"   3. Open code.js in your plugin folder")
    print(f"   4. Find this line:")
    print(f"      const ICONS_JSON = `PASTE_YOUR_ICONS_JSON_HERE`;")
    print(f"   5. Replace PASTE_YOUR_ICONS_JSON_HERE with the copied JSON")
    print(f"{'─'*50}\n")

if __name__ == "__main__":
    generate()