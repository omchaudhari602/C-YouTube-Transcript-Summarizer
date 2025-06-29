# Import all the necessary dependencies
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import google.generativeai as genai
application = Flask(__name__)
genai.configure(api_key="AIzaSyBm0u5pkLLkcIDS-5M9xCrEfuURbuopyPM")
@application.get('/summary')
def summary_api():
    
    url = request.args.get('url', '')
    max_length = int(request.args.get('max_length', 100))
    video_id = url.split('=')[1]

    try:
        transcript = get_transcript(video_id)
        print(transcript)
    except:
        return "No subtitles available for this video", 404

    x=chat(transcript=transcript,maxlen=max_length)
    print(x)
    return x, 200

def chat(transcript,maxlen):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(transcript + " summarize this youtube transcipt in "+str(maxlen)+" words")
       
    return response.text

def is_transcript_english(transcript):
    try:
        language = detect(transcript)
        return language == 'en'
    
    except Exception as e:
        return False

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise e

    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

if __name__ == '__main__':
    application.run(debug=True)
