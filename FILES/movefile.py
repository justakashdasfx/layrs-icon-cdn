"""
movefile.py
-----------
Moves ALL .svg files from any subfolder depth
into the same folder where this script is located.
Then deletes ALL subfolders and this script itself.

Usage:
    1. Put this file inside the folder you want to flatten
       e.g. Icons/Hugeicon Rounded/Stroke/
    2. Run: python movefile.py
"""

import os
import shutil

# Folder where this script lives
ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.abspath(__file__)

moved = 0
conflicts = []

# ── Step 1: Move all SVGs to ROOT ──────────────────────
for dirpath, dirnames, filenames in os.walk(ROOT):
    if dirpath == ROOT:
        continue

    for filename in filenames:
        if not filename.endswith('.svg'):
            continue

        src = os.path.join(dirpath, filename)
        dst = os.path.join(ROOT, filename)

        if os.path.exists(dst):
            base = filename[:-4]
            counter = 1
            while os.path.exists(os.path.join(ROOT, f"{base}__{counter}.svg")):
                counter += 1
            dst = os.path.join(ROOT, f"{base}__{counter}.svg")
            conflicts.append(filename)

        shutil.move(src, dst)
        moved += 1

# ── Step 2: Delete ALL subfolders ──────────────────────
deleted_folders = 0
for item in os.listdir(ROOT):
    item_path = os.path.join(ROOT, item)
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)
        deleted_folders += 1
        print(f"   🗑️  Deleted folder: {item}")

# ── Step 3: Print results ───────────────────────────────
print(f"\n✅  Done!")
print(f"   📄  {moved} SVG files moved")
print(f"   🗑️  {deleted_folders} folders deleted")
if conflicts:
    print(f"   ⚠️  {len(conflicts)} renamed (duplicates): {conflicts[:5]}{'...' if len(conflicts) > 5 else ''}")

# ── Step 4: Delete this script ─────────────────────────
os.remove(SCRIPT)
print(f"   🗑️  movefile.py deleted")