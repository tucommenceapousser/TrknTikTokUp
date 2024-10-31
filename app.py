import streamlit as st
import openai
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
import os
import requests
import tempfile
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration des dossiers
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dossier pour stocker les fichiers temporaires
if not os.path.exists("static"):
    os.makedirs("static")

# Fonction pour générer la voix à partir de texte avec Eleven Labs
def generate_voice_eleven_labs(text, filename="static/audio.mp3"):
    api_url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Authorization": f"Bearer {os.getenv('ELEVEN_LABS_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": "elevenlabs-voice-id",
        "model_id": "elevenlabs-model-id"
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        st.error(f"Erreur lors de la génération de la voix: {response.status_code}, {response.text}")
        return None

    return filename

# Fonction pour créer la vidéo
def create_video(image_path, audio_path, text, output="static/output_video.mp4"):
    image_clip = ImageClip(image_path).set_duration(10)
    text_clip = TextClip(text, fontsize=24, color='white', font="Arial-Bold", bg_color="#ff005a")
    text_clip = text_clip.set_position("center").set_duration(10).crossfadein(1).crossfadeout(1)
    audio_clip = AudioFileClip(audio_path)
    video = CompositeVideoClip([image_clip, text_clip])
    video = video.set_audio(audio_clip)
    video.write_videofile(output, fps=24)
    return output

# Fonction pour obtenir une image via DALL-E
def generate_image(prompt, filename="static/image.png"):
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(image_data)
    return filename

# Fonction de transcription
def transcribe_audio(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file, language="fr")
        return transcript.get('text', '')
    except Exception as e:
        st.error(f"Erreur de transcription: {str(e)}")
        return "Erreur lors de la transcription"

def process_video_file(video_file_path):
    try:
        temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        video_clip = VideoFileClip(video_file_path)
        video_clip.audio.write_audiofile(temp_audio.name)
        video_clip.close()
        transcription = transcribe_audio(temp_audio.name)
        os.unlink(temp_audio.name)
        return transcription
    except Exception as e:
        st.error(f"Erreur de traitement vidéo: {str(e)}")
        return "Erreur lors du traitement de la vidéo"

# Interface Streamlit
st.set_page_config(page_title="Optimiseur de contenu TikTok", page_icon="🎥")
st.title("🎬 Optimiseur de contenu TikTok")
st.subheader("Téléchargez votre fichier audio ou vidéo et optimisez votre contenu!")

# Uploader le fichier
media_file = st.file_uploader("Choisissez un fichier audio ou vidéo", type=['mp4', 'mov', 'avi', 'mp3', 'wav'])

# Champs de texte
content = st.text_area("Entrez votre description TikTok originale")
image_theme = st.text_input("Thème de l'image à générer")

if st.button("Optimiser le contenu"):
    if media_file:
        filename = media_file.name
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(media_file.getbuffer())

        transcription_text = ""
        if filename.lower().endswith(('.mp4', '.mov', '.avi')):
            transcription_text = process_video_file(file_path)
        else:
            transcription_text = transcribe_audio(file_path)

        # Optimisation avec GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en optimisation de contenu TikTok."},
                {"role": "user", "content": f"""Optimise cette description TikTok en te basant sur:
                - Description originale: {content}
                - Transcription: {transcription_text}

                Rends-la plus engageante et virale."""}
            ],
            max_tokens=100,
            temperature=0.7
        )
        suggestion = response['choices'][0]['message']['content'].strip()

        # Génération de l'image et de la voix
        image_path = generate_image(image_theme)
        audio_path = generate_voice_eleven_labs(suggestion)

        # Création de la vidéo
        video_path = create_video(image_path, audio_path, suggestion)

        # Affichage des résultats
        st.success("Optimisation terminée!")
        st.subheader("Suggestion optimisée:")
        st.write(suggestion)
        st.subheader("Transcription:")
        st.write(transcription_text)

        st.video(video_path)

    else:
        st.error("Veuillez télécharger un fichier audio ou vidéo.")

if st.button("Réinitialiser"):
    st.experimental_rerun()
