#!/usr/bin/env python3
import json
from pathlib import Path
import random

def main():
    print("=== [V2026] Directeur Créatif Multilingue & Architecte de Scène ===")
    base_dir = Path(__file__).resolve().parent.parent
    config_dir = base_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    languages = [
        {"code": "ar-XA", "name": "Arabic", "greeting": "مرحباً بكم يا أصدقائي في مغامرتنا اليوم!"},
        {"code": "en-US", "name": "English", "greeting": "Welcome my friends to our magical adventure today!"},
        {"code": "fr-FR", "name": "French", "greeting": "Bienvenue mes amis dans notre aventure magique !"}
    ]
    selected_lang = random.choice(languages)
    
    universes = [
        {
            "theme": "سر البيت العتيق في المدينة الساحلية",
            "setting": "أزقة مدينة مغربية تقليدية بمعمار أبيض وأزرق وأقواس عتيقة",
            "architecture_style": "Traditional Moroccan Riad / Coastal Architecture"
        },
        {
            "theme": "مغامرة الغابة المضيئة والأشجار العريقة",
            "setting": "غابة خيالية عميقة تكسوها الأشجار الضخمة والنباتات المضيئة",
            "architecture_style": "Enchanted Forest Organic Architecture"
        }
    ]
    selected_univ = random.choice(universes)
    
    blueprint = {
        "theme": selected_univ["theme"],
        "language": selected_lang["name"],
        "lang_code": selected_lang["code"],
        "setting_description": selected_univ["setting"],
        "architecture_style": selected_univ["architecture_style"],
        "cast": ["Yakine", "Nour", "Grandma"]
    }
    
    (config_dir / "scene_design_blueprint.json").write_text(json.dumps(blueprint, indent=4, ensure_ascii=False), encoding="utf-8")
    
    creative_script = [
        {
            "character": "Yakine",
            "type": "dialogue",
            "language": selected_lang["code"],
            "text": selected_lang["greeting"] + f" ({selected_univ['theme']})"
        },
        {
            "character": "Nour",
            "type": "song",
            "language": selected_lang["code"],
            "text": "<speak><prosody rate='slow' pitch='+3st'>نحلق فوق الأفق البعيد، ننشر للأحلام نشيداً جديداً!</prosody></speak>"
        }
    ]
    
    (config_dir / "scenario_script.json").write_text(json.dumps(creative_script, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Langue : {selected_lang['name']} | Thème : {selected_univ['theme']}")

if __name__ == "__main__":
    main()
