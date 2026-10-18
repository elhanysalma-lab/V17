#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    print("=== [Agent Autonome 12 FPS] Coordination et Gestion du Framerate ===")
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / "config"
    script_path = config_dir / "scenario_script.json"
    
    if script_path.exists():
        script_data = json.loads(script_path.read_text(encoding="utf-8"))
        print(f"✓ {len(script_data)} scènes chargées. Mode d'affichage: 12 FPS (On-Twos Classic Cel-Animation).")
    else:
        print("⚠️ Script introuvable pour l'analyse autonome.")

if __name__ == "__main__":
    main()
