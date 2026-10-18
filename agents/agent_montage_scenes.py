#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    output_dir = base_dir / "output_movies"
    scenes_dir = base_dir / "temp_scenes"
    config_file = base_dir / "config" / "timeline.json"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    scenes_dir.mkdir(parents=True, exist_ok=True)
    
    if not config_file.exists():
        print("Erreur: timeline.json manquant.")
        return
        
    timeline = json.loads(config_file.read_text(encoding="utf-8"))
    concat_list_path = scenes_dir / "concat_list.txt"
    
    print("Démarrage de la génération des scènes (12 FPS, avec piste audio muette pour YouTube)...")
    
    with open(concat_list_path, "w") as concat_file:
        for scene in timeline:
            char_img = assets_dir / scene["character"]
            scene_mp4 = scenes_dir / f"scene_{scene['scene_id']}.mp4"
            dur = scene["duration_seconds"]
            bg = scene["bg_color"]
            
            print(f"-> Rendu de la scène {scene['scene_id']} (Durée: {dur}s)...")
            
            if char_img.exists():
                # FFmpeg: Crée un fond, superpose l'image centrée, force 12 FPS, et ajoute une piste audio silencieuse
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi", "-i", f"color=c={bg}:s=1280x720:d={dur}",
                    "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100:d={dur}",
                    "-loop", "1", "-t", str(dur), "-i", str(char_img),
                    "-filter_complex", 
                    "[2:v]scale=720:-1[char];[0:v][char]overlay=(W-w)/2:(H-h)/2:shortest=1,fps=12[vout]",
                    "-map", "[vout]", "-map", "1:a",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    str(scene_mp4)
                ]
            else:
                # Si l'image manque, on met un fond de couleur avec le texte au lieu d'une erreur
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi", "-i", f"color=c={bg}:s=1280x720:d={dur}",
                    "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100:d={dur}",
                    "-filter_complex", f"drawtext=text='Personnage manquant':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2,fps=12[vout]",
                    "-map", "[vout]", "-map", "1:a",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    str(scene_mp4)
                ]
            
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            concat_file.write(f"file '{scene_mp4.name}'\n")
            
    print("\nFusion (Concaténation) des scènes pour créer le film complet...")
    final_output = output_dir / "noury_pixar_4minutes_youtube.mp4"
    
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(final_output)
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✓ SUCCÈS : Vidéo longue durée générée -> {final_output}")

if __name__ == "__main__":
    main()
