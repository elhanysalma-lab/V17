#!/usr/bin/env python3
from pathlib import Path
try:
    from PIL import Image, ImageFilter
except ImportError:
    Image = None

def main():
    print("=== [12 FPS] Traitement des Personnages & Normal Maps ===")
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    if Image is None:
        return
    for img_path in assets_dir.glob("*.png"):
        if "_normal" in img_path.name:
            continue
        try:
            im = Image.open(img_path).convert("RGBA")
            im.convert("L").filter(ImageFilter.FIND_EDGES).save(assets_dir / f"{img_path.stem}_normal.png")
            print(f"✓ Normal map générée pour : {img_path.name}")
        except Exception as e:
            print(f"⚠️ Erreur: {e}")

if __name__ == "__main__":
    main()
