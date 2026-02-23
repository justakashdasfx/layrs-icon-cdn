"""
generate_manifest.py — DEBUG VERSION
Run from the ROOT of your layrs-icon-cdn repo.
Usage: python generate_manifest.py
"""

import os
import json

OUTPUT_FILE = "manifest.json"

def find_icons_dir():
    for name in ["Icons", "icons", "ICONS"]:
        if os.path.exists(name):
            return name
    return None

def generate():
    icons_dir = find_icons_dir()

    if not icons_dir:
        print("❌  No icons folder found. Make sure you're running from the repo root.")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Files here: {os.listdir('.')}")
        return

    print(f"📁  Found icons folder: '{icons_dir}'")
    print(f"📁  Current dir: {os.getcwd()}\n")

    libraries = {}

    for library in sorted(os.listdir(icons_dir)):
        lib_path = os.path.join(icons_dir, library)
        if not os.path.isdir(lib_path) or library.startswith('.'):
            continue

        libraries[library] = {}
        print(f"📦  Library: {library}")

        for category in sorted(os.listdir(lib_path)):
            cat_path = os.path.join(lib_path, category)
            if not os.path.isdir(cat_path) or category.startswith('.'):
                continue

            icons = []
            svg_count = 0

            for root, dirs, files in os.walk(cat_path):
                dirs[:] = [d for d in sorted(dirs) if not d.startswith('.')]
                svgs = [f for f in files if f.endswith('.svg') and not f.startswith('.')]
                svg_count += len(svgs)
                for filename in svgs:
                    icon_name = filename[:-4]
                    icons.append(icon_name)

            icons = sorted(list(dict.fromkeys(icons)))
            libraries[library][category] = icons

            # Debug: show first subfolder contents
            sub_items = [x for x in os.listdir(cat_path) if not x.startswith('.')]
            print(f"   [{category}] → {len(icons)} icons | contains: {sub_items[:3]}{'...' if len(sub_items) > 3 else ''}")

            # If still 0, go one level deeper and report
            if len(icons) == 0 and sub_items:
                first_sub = os.path.join(cat_path, sub_items[0])
                if os.path.isdir(first_sub):
                    deep = os.listdir(first_sub)
                    print(f"      ↳ Inside '{sub_items[0]}': {deep[:5]}")

    manifest = { "version": "1.0.0", "libraries": libraries }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    total = sum(len(v) for lib in libraries.values() for v in lib.values())
    print(f"\n✅  Done — {total} icons total")

if __name__ == "__main__":
    generate()