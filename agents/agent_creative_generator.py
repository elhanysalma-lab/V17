#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    print("=== [V2026] Directeur Créatif & Paramétrage 12 FPS ===")
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    blueprint = {
        "theme": "سر البيت العتيق في المدينة الساحلية",
        "language": "Arabic",
        "lang_code": "ar-XA",
        "framerate": 12,
        "animation_style": "Classic Cel-Animation 12 FPS On-Twos",
        "setting_description": "أزقة مدينة مغربية تقليدية بمعمار أبيض وأزرق",
        "cast": ["Yakine", "Nour", "Grandma"]
    }
    (config_dir / "scene_design_blueprint.json").write_text(json.dumps(blueprint, indent=4, ensure_ascii=False), encoding="utf-8")
    
    script = [
        {"character": "Nour", "type": "dialogue", "text": "مرحباً بكم يا أصدقائي في مغامرتنا اليوم!"},
        {"character": "Yakine", "type": "song", "text": "<speak><prosody rate='slow' pitch='+4st'>نحلق فوق الأفق البعيد، ننشر للأحلام نشيداً جديداً!</prosody></speak>"}
    ]
    (config_dir / "scenario_script.json").write_text(json.dumps(script, indent=4, ensure_ascii=False), encoding="utf-8")
    print("✓ Blueprint et Script 12 FPS générés (Yakine=Fille, Nour=Garçon).")

if __name__ == "__main__":
    main()
