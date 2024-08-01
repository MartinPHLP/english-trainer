import os
import time
import wave
import json
import pygame
import pyaudio
import threading
import subprocess

from openai import OpenAI
from pynput import keyboard


class AudioHandler:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.WAV_USER_PATH = "./audio/output.wav"
        self.ERROR_SOUD_PATH = "./audio/error.mp3"
        self.SPEECH_OUTPUT_PATH = "./audio/speech.mp3"
        self.openai_client = OpenAI()
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)

    def record_audio(self):
        self.frames = []
        while self.recording:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            self.frames.append(data)

    def on_press(self, key):
        if key == keyboard.Key.space:
            if not self.recording:
                self.recording = True
                threading.Thread(target=self.record_audio).start()
            else:
                self.recording = False
                self.save_audio()
                return False

    def save_audio(self):
        with wave.open(self.WAV_USER_PATH, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))

    def listen_and_transcribe(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        return self.transcribe_audio()

    def transcribe_audio(self):
        WHISPER_MAIN_PATH = "./whisper.cpp/main"
        WHISPER_MODEL_PATH = "./whisper.cpp/models/ggml-base.en.bin"

        command = f"{WHISPER_MAIN_PATH} -m {WHISPER_MODEL_PATH} -f {self.WAV_USER_PATH} -oj -of {os.getenv('WHISPER_OUTPUT_PATH')}"
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.5)

        with open(os.getenv("WHISPER_OUTPUT_PATH") + ".json", "r") as file:
            output_json = json.load(file)
            user_text = output_json["transcription"][0]["text"]

        return user_text

    def synthesize_speech(self, inputs):

        text = inputs["messages"][-1].content
        voice = inputs["voice"]
        response = self.openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        response.stream_to_file(self.SPEECH_OUTPUT_PATH)
        return {
            "messages": inputs["messages"],
            "ai_response": inputs["ai_response"],
            "user_input": inputs["user_input"],
            "voice": inputs["voice"],
            "correction": inputs["correction"]
        }

    def play_audio(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)
