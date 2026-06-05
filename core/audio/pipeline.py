import asyncio
import numpy as np
import sounddevice as sd
import torch
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from whisper_cpp_python import Whisper
import onnxruntime as ort
import os

class AudioPipeline:
    def __init__(self, sample_rate=16000, chunk_size=512):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.buffer = np.zeros(0, dtype=np.float32)
        
        # Load Silero VAD (placeholder for ONNX model)
        # self.vad_session = ort.InferenceSession("silero_vad.onnx")
        
        # Load Whisper (placeholder path)
        # self.asr = Whisper(model_path="ggml-distil-large-v3.bin")
        
        # Load ECAPA-TDNN for Speaker Verification
        self.speaker_classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
        self.owner_voice_tensor = None
        if os.path.exists("config/owner_voice.pt"):
            self.owner_voice_tensor = torch.load("config/owner_voice.pt")
            
    def audio_callback(self, indata, frames, time, status):
        """Called for each audio block."""
        if status:
            print(status)
        self.buffer = np.append(self.buffer, indata[:, 0])
        
    def start_listening(self):
        self.stream = sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self.audio_callback)
        self.stream.start()
        
    def stop_listening(self):
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()

    def process_buffer(self):
        """Returns transcribed text if valid speaker"""
        # 1. Run VAD
        # 2. Extract Speech Segment
        speech = self.buffer # Simplified
        
        # 3. Speaker Verification
        if self.owner_voice_tensor is not None:
            tensor = torch.tensor(speech).unsqueeze(0)
            embeddings = self.speaker_classifier.encode_batch(tensor)
            similarity = torch.nn.functional.cosine_similarity(embeddings, self.owner_voice_tensor, dim=-1)
            if similarity.item() < 0.82:
                print("Speaker verification failed.")
                return None
                
        # 4. ASR
        # text = self.asr.transcribe(speech)
        text = "Test command" # Mock transcription
        
        # Clear buffer
        self.buffer = np.zeros(0, dtype=np.float32)
        return text

    async def run(self, callback):
        self.start_listening()
        print("Listening...")
        try:
            while True:
                await asyncio.sleep(1) # simulate chunk processing
                if len(self.buffer) > self.sample_rate * 3: # Process every 3 seconds
                    text = self.process_buffer()
                    if text:
                        await callback(text)
        except asyncio.CancelledError:
            self.stop_listening()
