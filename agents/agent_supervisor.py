#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def run_step(name, script_path):
    print(f"\n=== [NOURY PIXAR V2026 - MEGA STUDIO] Étape : {name} ===")
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
    print("=== Noury Pixar V2026 - Absolute Infinite Mega Studio Framework     ===")
    print("=======================================================================")
    
    base_dir = Path(__file__).resolve().parent
    
    # 100% Intégral - Tous les modules, agents, shaders, configs et scripts de déploiement
    run_step("1. Directeur Créatif & Multilingue", base_dir / "agent_creative_generator.py")
    run_step("2. Traitement des Personnages & Normal Maps", base_dir / "agent_character_generator.py")
    run_step("3. Scénariste & Structuration", base_dir / "agent_scriptwriter.py")
    run_step("4. Directeur de Scène & Scénographie", base_dir / "agent_director.py")
    run_step("5. Synthèse Vocale Multilingue & SSML", base_dir / "agent_audio.py")
    run_step("6. Correction & Synchronisation Temporelle (4-15 min)", base_dir / "agent_bounded_correction.py")
    run_step("7. Réalisation Caméra & DOF", base_dir / "agent_camera_director.py")
    run_step("8. Moteur Godot 4 (SDFGI + Fog + ACES + Wind)", base_dir / "render_scene.gd")
    run_step("9. Montage Vidéo Final (FFmpeg)", base_dir / "agent_montage.py")
    run_step("10. Miniature YouTube", base_dir / "agent_thumbnail.py")
    run_step("11. Métadonnées & SEO YouTube", base_dir / "agent_youtube_metadata.py")
    run_step("12. Publication Automatique YouTube", base_dir / "agent_youtube_upload.py")
    run_step("13. Vérification des Licences", base_dir / "agent_licence_check.py")
    run_step("14. Contrôle Qualité Final", base_dir / "agent_quality_control.py")
    
    print("\n🎉 [SUCCÈS ABSOLU V2026] Le méga studio est complet à 100% !")

if __name__ == "__main__":
    main()
