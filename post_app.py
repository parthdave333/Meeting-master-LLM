from flask import Flask, request, render_template, redirect, url_for
from moviepy.editor import VideoFileClip
import assemblyai as aai
import cohere
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AssemblyAI and Cohere API Keys
aai.settings.api_key = 'c49fa46ebb33448498380d959bb8ac33'
cohere_api_key = 'qzxcsxL1fhLcgRFcKXjqCnNWVwI3nr9dO3JPt8Zg'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_audio(video_path, audio_output_path):
    """Converts video file to mp3 audio."""
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
        print(f"Audio extracted and saved to: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

def transcribe_audio(audio_path):
    """Transcribes the audio to text using AssemblyAI."""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    return transcript.text

def summarize_text(text):
    """Summarizes the text using Cohere in a structured format (Agenda, Key Points, Conclusion)."""
    co = cohere.Client(cohere_api_key)

    # Check if the text is long enough for summarization
    if len(text) < 250:
        return "Text is too short for summarization. Here's the full text:\n\n" + text

    # Create a prompt to guide the model to produce a structured summary
    structured_prompt = (
        "Please summarize the following meeting transcript in a structured format with the following sections:\n\n"
        "1. Agenda of the Meeting\n"
        "2. Key Discussion Points\n"
        "3. Conclusion of the Meeting\n\n"
        f"Transcript: {text}\n\n"
        "Provide the summary in bullet points under each section."
    )

    # Use the correct Cohere model to generate the structured summary
    response = co.generate(
        model='command-xlarge-nightly',  # Or replace with another valid model
        prompt=structured_prompt,
        max_tokens=500,  # Limit tokens to control the length of the response
        temperature=0.5,  # Lower temperature for more structured output
        stop_sequences=["Conclusion:"]  # Stop after generating the conclusion
    )

    # Return the generated structured summary
    return response.generations[0].text

@app.route('/', methods=['GET'])
def index():
    return render_template('post_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return 'No file uploaded', 400

    video = request.files['video']
    if video.filename == '':
        return 'No file selected', 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)

    # Convert video to audio (mp3)
    audio_output_path = video_path.replace('.mp4', '.mp3')
    extract_audio(video_path, audio_output_path)

    # Transcribe audio to text
    transcript = transcribe_audio(audio_output_path)

    # Summarize the transcribed text in a structured format
    summary = summarize_text(transcript)

    # Return the structured summary as the result
    return f"<h1>Summary</h1><pre>{summary}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
