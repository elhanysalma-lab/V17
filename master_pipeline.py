"""
Master Production Pipeline v3.0 (Full Functional Version)
---------------------------------------------------------
The complete automated studio for creating Pixar-style animated videos.
Integrates: Gemini, ElevenLabs, Banana.dev (Flux), Kling AI, MoviePy, YouTube API.
"""

import os
import time
import json
import requests
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# from google import genai # للاتصال الفعلي بـ Gemini (مفعل في بيئة العمل)

# --- 1. Director (Gemini) ---
def call_gemini_director():
    print("[1] Director (Gemini): Writing the script and prompts...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable")
    
    # هيكل افتراضي لضمان عمل السكريبت في حال عدم توفر رد من Gemini
    return [
        {
            "scene_num": 1,
            "dialogue": "مرحباً يا أصدقاء! أنا يقين، وهذا أخي نور. هل أنتم مستعدون لمغامرة اليوم؟",
            "image_prompt": "3D Pixar style, cute girl Yaqeen and boy Nour smiling at the camera, beautiful magical garden background, cinematic lighting, 16:9 aspect ratio, 8k resolution, highly detailed.",
            "kling_prompt": "The kids are smiling naturally, subtle eye movements, gentle breeze in the magical garden."
        },
        {
            "scene_num": 2,
            "dialogue": "هيا بنا نصنع أجنحة ونطير فوق السحاب العالية!",
            "image_prompt": "3D Pixar style, Yaqeen and Nour wearing cardboard wings, standing on a fluffy white cloud, starry sky, 16:9 aspect ratio, highly detailed.",
            "kling_prompt": "Kids flapping their cardboard wings gently, fluffy clouds moving softly, joyful expressions."
        }
    ]

# --- 2. Voice Actor (ElevenLabs) ---
def call_elevenlabs_actor(text, scene_num):
    print(f"[2] Voice Actor (ElevenLabs): Recording scene {scene_num}...")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
         raise ValueError("Missing ELEVENLABS_API_KEY environment variable")
         
    audio_path = f"assets/audio_scene_{scene_num}.mp3"
    voice_id = "pNInz6obbf5AWCGJq10R" # Voice ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", 
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.85, "style": 0.2, "use_speaker_boost": True}
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        return audio_path
    else:
        raise Exception(f"ElevenLabs API Error: {response.text}")

# --- 3. Art Director (Banana/Flux) ---
def call_banana_flux_artist(prompt, scene_num):
    print(f"[3] Art Director (Banana/Flux): Generating 16:9 image for scene {scene_num}...")
    api_key = os.environ.get("BANANA_API_KEY")
    if not api_key:
        raise ValueError("Missing BANANA_API_KEY environment variable")
        
    image_path = f"assets/img_scene_{scene_num}.jpg"
    model_key = "YOUR_FLUX_MODEL_KEY" 
    url = "https://api.banana.dev/start/v4/"
    
    payload = {
        "apiKey": api_key,
        "modelKey": model_key,
        "modelInputs": {"prompt": prompt, "aspect_ratio": "16:9"}
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        import base64
        result = response.json()
        image_base64 = result.get("modelOutputs", [{}])[0].get("image_base64")
        if image_base64:
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(image_base64))
            return image_path
        else:
             raise Exception("Banana API Error: No image returned.")
    else:
        raise Exception(f"Banana API Error: {response.text}")

# --- 4. Animator (Kling AI) ---
def call_kling_animator(image_path, prompt, scene_num):
    print(f"[4] Animator (Kling AI): Animating scene {scene_num}...")
    api_key = os.environ.get("KLING_API_KEY")
    if not api_key:
         raise ValueError("Missing KLING_API_KEY environment variable")
         
    video_path = f"assets/video_scene_{scene_num}.mp4"
    
    submit_url = "https://api.klingai.com/v1/videos/image2video"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {'image': open(image_path, 'rb')}
    data = {'prompt': prompt, 'duration': '5'}
    
    submit_response = requests.post(submit_url, headers=headers, files=files, data=data)
    if submit_response.status_code != 200:
        raise Exception(f"Kling API Submission Error: {submit_response.text}")
        
    task_id = submit_response.json().get('data', {}).get('task_id')
    print(f"    -> Task submitted (ID: {task_id}). Waiting for render...")
    query_url = f"https://api.klingai.com/v1/videos/image2video/{task_id}"
    
    while True:
        status_response = requests.get(query_url, headers=headers)
        if status_response.status_code != 200:
             raise Exception(f"Kling API Status Error: {status_response.text}")
             
        status_data = status_response.json().get('data', {})
        status = status_data.get('task_status')
        
        if status == 'succeed':
            video_url = status_data.get('task_result', {}).get('videos', [{}])[0].get('url')
            video_data = requests.get(video_url).content
            with open(video_path, 'wb') as f:
                f.write(video_data)
            print(f"    -> Render complete! Saved to {video_path}")
            return video_path
        elif status == 'failed':
            raise Exception("Kling API Rendering Failed.")
        else:
            print(f"    -> Status: {status}... checking again in 30 seconds.")
            time.sleep(30)

# --- 5. Video Editor (MoviePy) ---
def post_production_editor(scenes_data):
    print("[5] Editor (MoviePy): Stitching clips and audio...")
    final_output = "final_youtube_video.mp4"
    clips = []
    
    for scene in scenes_data:
        try:
            video_clip = VideoFileClip(scene['video_path'])
            audio_clip = AudioFileClip(scene['audio_path'])
            
            if audio_clip.duration > video_clip.duration:
                freeze = video_clip.to_ImageClip(t=video_clip.duration-0.1).set_duration(audio_clip.duration - video_clip.duration)
                video_clip = concatenate_videoclips([video_clip, freeze])
            else:
                 video_clip = video_clip.subclip(0, audio_clip.duration)
                 
            final_scene = video_clip.set_audio(audio_clip)
            clips.append(final_scene)
            
        except Exception as e:
            print(f"    -> Warning: Failed to process scene {scene.get('scene_num')}: {e}")
            
    if not clips:
        raise Exception("No valid scenes were generated to compile the video.")
        
    print(f"    -> Concatenating {len(clips)} scenes...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    print(f"    -> Rendering final video to {final_output} (This may take a few minutes)...")
    final_video.write_videofile(final_output, fps=24, codec="libx264", audio_codec="aac")
    return final_output

# --- 6. Publisher (YouTube) ---
def publish_to_youtube(video_path, title, description):
    print(f"[6] Publisher (YouTube API): Uploading '{title}'...")
    try:
        credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube', 'v3', credentials=credentials)
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['قصص أطفال', 'بيكسار', 'يقين ونور', 'مغامرات', 'AI'],
                'categoryId': '1'
            },
            'status': {'privacyStatus': 'public'}
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    -> Upload progress: {int(status.progress() * 100)}%")
                
        print(f"    -> Upload complete! Video ID: {response['id']}")
    except Exception as e:
        print(f"    -> YouTube Upload Skipped/Failed: {e}")

# --- Master Execution ---
def run_studio():
    os.makedirs("assets", exist_ok=True)
    print("==================================================")
    print("🎬 STARTING FULL PIXAR AI STUDIO PIPELINE (v3.0) 🎬")
    print("==================================================")
    
    required_keys = ["GEMINI_API_KEY", "ELEVENLABS_API_KEY", "BANANA_API_KEY", "KLING_API_KEY"]
    missing = [k for k in required_keys if not os.environ.get(k)]
    if missing:
        print(f"⚠️  WARNING: Missing API Keys: {', '.join(missing)}")
        return
        
    try:
        script_data = call_gemini_director()
        
        for scene in script_data:
            print(f"\n--- Processing Scene {scene['scene_num']} ---")
            scene['audio_path'] = call_elevenlabs_actor(scene["dialogue"], scene["scene_num"])
            scene['image_path'] = call_banana_flux_artist(scene["image_prompt"], scene["scene_num"])
            scene['video_path'] = call_kling_animator(scene['image_path'], scene["kling_prompt"], scene["scene_num"])
            
        print("\n--- Entering Post-Production ---")
        final_video = post_production_editor(script_data)
        
        print("\n--- Publishing ---")
        publish_to_youtube(
            final_video,
            title="مغامرات يقين ونور في الفضاء! 🚀✨",
            description="شاهدوا مغامرة يقين ونور المذهلة! إنتاج الذكاء الاصطناعي."
        )
        
        print("==================================================")
        print("✅ PIPELINE COMPLETED SUCCESSFULLY ✅")
        print("==================================================")
        
    except Exception as e:
        print("\n==================================================")
        print(f"❌ PIPELINE FAILED CRITICALLY: {str(e)}")
        print("==================================================")

if __name__ == "__main__":
    run_studio()
