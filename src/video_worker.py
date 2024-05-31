from googletrans import Translator  
from gtts import gTTS  
import moviepy.editor as mp 
import requests
from PIL import Image
import pytesseract
import speech_recognition as sr 
import json
import base64

languade_to_translat = 'ca'
cutted_audio_name = 'cutted_audio.mp3'
cutted_audio_translated_name = 'cutted_audio_translated.mp3'
first_frame_name = 'first_frame.jpg'
url_video = 'video.mp4'
wav_file = 'cutted_audio.wav'


class VideoWorker():
    url = ''
    pixels_tall = 0
    duration = 0
    translated_text = ''
    first_frame_image_text = ''
    image_data = {}

    @classmethod
    def set_url(self, url):
        if url != self.url:
            self.url = url
            self.download_mp4_from_url(url, url_video)

            video = mp.VideoFileClip(url_video)
            audio_file = self.get_cut_video(30, 45, video).audio 


            self.duration = video.duration
            self.pixels_tall = video.size[1]

            self.translate_audio_to_spanish(audio_file)
            self.image_data = self.get_text_from_image(video)
        return {'url': self.url, 'duration': self.duration, 
        'pixelsTall': self.pixels_tall, 'image': self.image_data}
    
    @classmethod
    def get_cached_data(self):
        return {'url': self.url, 'duration': self.duration, 
        'pixelsTall': self.pixels_tall, 'image': self.image_data}

    def get_cut_video(startTime, endTime, video):
        clip = video.subclip(startTime, endTime)
        return clip

    def translate_audio_to_spanish(audio_file):
        #Checkpoint 4
        translator = Translator()
        
        audio_file.write_audiofile(wav_file) 
        r = sr.Recognizer() 
        with sr.AudioFile(wav_file) as source: 
            original_audio = r.record(source) 
            
        with open(wav_file, "wb") as file:
            file.write(original_audio.get_wav_data())

        text = r.recognize_google(original_audio)
        translation = translator.translate(text, dest='ca')
        speak = gTTS(text=translation.text, lang='ca', slow=False) 
        speak.save(cutted_audio_translated_name)

         

    def stream_original_audio():
        #Checkpoint 5
        with open(wav_file, mode="rb") as file:
            yield from file

    def stream_translated_audio():
        #Checkpoint 5
        with open(cutted_audio_translated_name, mode="rb") as file:
            yield from file
            

    def get_text_from_image(clip):
        #Checkpoint 7
        clip.save_frame(first_frame_name)
        img = Image.open(first_frame_name)
        text = pytesseract.image_to_string(img)

        with open(first_frame_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        return {'text': text, 'base64': encoded_string}

    def download_mp4_from_url(url, file_name):
        resp = requests.get(url) # making requests to server

        with open(file_name, "wb") as f: # opening a file handler to create new file 
            f.write(resp.content) 