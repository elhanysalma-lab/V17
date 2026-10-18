#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def run_step(name, script_path):
    print(f"\n=== [NOURY PIXAR] Étape : {name} ===")
    if not script_path.exists():
        print(f"⚠️ {script_path.name} introuvable.")
        return
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Erreur critique :\n{result.stderr}")
        sys.exit(result.returncode)

def main():
    print("=======================================================================")
    print("=== Noury Pixar Studio - Moteur de Production 4-15 Minutes          ===")
    print("=======================================================================")
    base_dir = Path(__file__).resolve().parent
    
    run_step("1. Génération du Scénario (Timeline)", base_dir / "agent_timeline.py")
    run_step("2. Moteur de Rendu des Scènes (FFmpeg 12 FPS)", base_dir / "agent_montage_scenes.py")
    
    print("\n🎉 [PIPELINE TERMINÉ] Vidéo longue durée générée avec succès !")

if __name__ == "__main__":
    main()
