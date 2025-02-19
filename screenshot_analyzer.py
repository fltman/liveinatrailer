from flask import Flask, request, jsonify, render_template
import base64
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
import pygame
import datetime

app = Flask(__name__)

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = "FF7KdobWPaiR0vkcALHF"  # Josh voice ID

def analyze_image(base64_image):
    """Send image to GPT-4V for analysis"""
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are the typical deep voiced movie trailer voice. everything is a cliffhanger. short and dramatic. Look at the content I provide (this could be code, text, images, or screenshots) and describe it as a  movie trailer cliffhanger.  1 to 3 short sentences"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image and provide feedback."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content

def get_audio(text):
    """Convert text to speech using ElevenLabs and return audio data"""
    eleven_labs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.95,
            "style": 0.47,
            "use_speaker_boost": True
        }
    }

    response = requests.post(eleven_labs_url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"ElevenLabs API error: {response.text}")
        
    return response.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data['image'].split(',')[1]  # Remove the data:image/jpeg;base64 prefix
        
        # Analyze the image
        analysis = analyze_image(image_data)
        
        # Get audio
        audio_data = get_audio(analysis)
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'audio': audio_base64
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 