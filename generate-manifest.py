"""
generate_manifest.py
--------------------
Run this script from the ROOT of your layrs-icon-cdn repo
whenever you add or remove icons.

Usage:
    python generate_manifest.py

It will scan the /icons folder and auto-generate manifest.json.
Then just commit and push — the plugin will pick up the changes.
"""

import os
import json

ICONS_DIR = "icons"
OUTPUT_FILE = "manifest.json"

def generate():
    libraries = {}

    if not os.path.exists(ICONS_DIR):
        print(f"❌  '{ICONS_DIR}' folder not found. Run this from the repo root.")
        return

    for library in sorted(os.listdir(ICONS_DIR)):
        lib_path = os.path.join(ICONS_DIR, library)
        if not os.path.isdir(lib_path):
            continue

        libraries[library] = {}

        for category in sorted(os.listdir(lib_path)):
            cat_path = os.path.join(lib_path, library, category)
            cat_path = os.path.join(lib_path, category)
            if not os.path.isdir(cat_path):
                continue

            icons = []
            for filename in sorted(os.listdir(cat_path)):
                if filename.endswith(".svg"):
                    icon_name = filename[:-4]  # strip .svg
                    icons.append(icon_name)

            libraries[library][category] = icons
            print(f"  ✓ {library}/{category}: {len(icons)} icons")

    manifest = {
        "version": "1.0.0",
        "libraries": libraries
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    total = sum(len(icons) for lib in libraries.values() for icons in lib.values())
    print(f"\n✅  manifest.json generated — {total} icons across {len(libraries)} libraries")

if __name__ == "__main__":
    generate()