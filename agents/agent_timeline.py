#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Conception mathématique d'une vidéo de 4 minutes (240 secondes)
    # Composée de 4 scènes de 60 secondes chacune pour YouTube Kids
    timeline = [
        {"scene_id": 1, "character": "1000096083_Yakine.png", "duration_seconds": 60, "bg_color": "0x1E293B", "action": "Intro & Accueil"},
        {"scene_id": 2, "character": "1000096078_Nour.png", "duration_seconds": 60, "bg_color": "0x331010", "action": "Histoire magique"},
        {"scene_id": 3, "character": "1000096068_Grandma.png", "duration_seconds": 60, "bg_color": "0x103310", "action": "Conseils & Sagesse"},
        {"scene_id": 4, "character": "1000096092_Puppy.png", "duration_seconds": 60, "bg_color": "0x332010", "action": "Conclusion et Au revoir"}
    ]
    
    timeline_file = config_dir / "timeline.json"
    timeline_file.write_text(json.dumps(timeline, indent=4), encoding="utf-8")
    print(f"✓ Timeline de 4 minutes (240s) générée dans {timeline_file.name}.")

if __name__ == "__main__":
    main()
