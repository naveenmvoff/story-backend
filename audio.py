# D:\LLM\LLMFinalEnhaceing\audio.py

import requests
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Get API Key from environment
API_KEY = os.getenv("MURF_API_KEY")

# Create audio directory if it doesn't exist
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio(text, language="ta"):
    print("step 1")
    if not API_KEY:
        print("step 1 - error: No API key found")
        return {"error": "API key not configured"}

    try:
        print("step 2")
        url = "https://api.murf.ai/v1/speech/generate"
        
        # Select voice based on language
        voice_id = "ta-IN-mani" if language == "ta" else "en-IN-aarav"
        print(f"Using voice ID: {voice_id}")
        
        payload = {
            "text": text,
            "voiceId": voice_id,
            "format": "MP3",
            "channel_type": "MONO",
            "sample_rate": 48000
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-key": API_KEY
        }

        print("step 3")
        response = requests.post(url, json=payload, headers=headers)
        
        print("step 4")
        print("step 4:", response)

        if response.status_code == 200:
            print("step 5")
            data = response.json()
            audio_url = data.get('audioFile')
            
            if audio_url:
                # Download and save the audio file
                audio_response = requests.get(audio_url)
                if audio_response.status_code == 200:
                    # Generate unique filename
                    filename = f"audio_{uuid.uuid4()}.mp3"
                    filepath = os.path.join(AUDIO_DIR, filename)
                    
                    # Save the file
                    with open(filepath, 'wb') as f:
                        f.write(audio_response.content)
                    
                    # Return the relative path
                    return f"/static/audio/{filename}"
                else:
                    return {"error": "Failed to download audio file"}
            
            print("step 5 - error")
            return {"error": "No audio URL in response"}
        else:
            print("step 5 - error")
            return {"error": f"API Error: {response.status_code} - {response.text}"}

    except requests.exceptions.RequestException as e:
        print(f"step 7 - Request error: {str(e)}")
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        print(f"step 8 - error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}
