#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def run_step(name, script_path):
    print(f"\n=== [NOURY PIXAR 12 FPS] Étape : {name} ===")
    if not script_path.exists():
        print(f"⚠️ Avertissement: {script_path} introuvable.")
        return
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Erreur critique dans {name}:\n{result.stderr}")
        sys.exit(result.returncode)
    print(f"✓ {name} exécuté avec succès.")

def main():
    print("=======================================================================")
    print("=== Noury Pixar Studio - 12 FPS Classic Animation Pipeline          ===")
    print("=======================================================================")
    
    base_dir = Path(__file__).resolve().parent
    
    run_step("1. Directeur Créatif & Multilingue", base_dir / "agent_creative_generator.py")
    run_step("2. Directeur Autonome (Supervision & Décisions)", base_dir / "agent_autonomous_director.py")
    run_step("3. Traitement des Personnages & Normal Maps", base_dir / "agent_character_generator.py")
    run_step("4. Scénariste & Structuration", base_dir / "agent_scriptwriter.py")
    run_step("5. Directeur de Scène & Scénographie", base_dir / "agent_director.py")
    run_step("6. Synthèse Vocale Multilingue & SSML", base_dir / "agent_audio.py")
    run_step("7. Correction & Synchronisation Temporelle (4-15 min)", base_dir / "agent_bounded_correction.py")
    run_step("8. Réalisation Caméra & DOF", base_dir / "agent_camera_director.py")
    run_step("9. Moteur Godot 4 (12 FPS Cel-Animation Setup)", base_dir / "render_scene.gd")
    run_step("10. Montage Vidéo Final (FFmpeg)", base_dir / "agent_montage.py")
    run_step("11. Miniature YouTube", base_dir / "agent_thumbnail.py")
    run_step("12. Métadonnées & SEO YouTube", base_dir / "agent_youtube_metadata.py")
    run_step("13. Publication Automatique YouTube", base_dir / "agent_youtube_upload.py")
    run_step("14. Vérification des Licences", base_dir / "agent_licence_check.py")
    run_step("15. Contrôle Qualité Final", base_dir / "agent_quality_control.py")
    
    print("\n🎉 [SUCCÈS ABSOLU] Le film 12 FPS est entièrement produit et prêt !")

if __name__ == "__main__":
    main()
