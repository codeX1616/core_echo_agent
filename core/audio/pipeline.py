import asyncio
import numpy as np
import sounddevice as sd
import torch
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
try:
    import whisper
    Whisper = whisper
except Exception as e:
    print(f"Warning: whisper library not found ({e}). Using mock ASR.")
    Whisper = None
import onnxruntime as ort
import os

class AudioPipeline:
    def __init__(self, sample_rate=16000, chunk_size=512):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.buffer = np.zeros(0, dtype=np.float32)
        
        # Load Silero VAD (placeholder for ONNX model)
        # self.vad_session = ort.InferenceSession("silero_vad.onnx")
        
        # Load Whisper
        if Whisper is not None:
            print("Loading Whisper model...")
            self.asr = Whisper.load_model("tiny")
        else:
            self.asr = None
        
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
        speech = self.buffer
        
        # 1. Simple Energy-Based VAD to ignore silence
        rms_energy = np.sqrt(np.mean(speech**2))
        if rms_energy < 0.01:
            self.buffer = np.zeros(0, dtype=np.float32)
            return None
            
        # 3. Speaker Verification
        if self.owner_voice_tensor is not None:
            tensor = torch.tensor(speech).unsqueeze(0)
            embeddings = self.speaker_classifier.encode_batch(tensor)
            similarity = torch.nn.functional.cosine_similarity(embeddings, self.owner_voice_tensor, dim=-1)
            if similarity.item() < 0.82:
                print("Speaker verification failed.")
                return None
                
        # 4. ASR
        if self.asr:
            try:
                # Whisper expects a 16kHz float32 numpy array
                result = self.asr.transcribe(speech, language="en")
                text = result.get("text", "").strip()
            except Exception as e:
                print(f"ASR Error: {e}")
                text = ""
        else:
            text = "Test command" # Fallback if library failed to load
            
        if not text:
            self.buffer = np.zeros(0, dtype=np.float32)
            return None
        
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
