import os
import numpy as np
import pywt
from torch.utils.data import Dataset
from moviepy.editor import *
from moviepy.video.fx.all import blackwhite
import librosa
from libs.Lsh import *
from tqdm import tqdm
import multiprocessing
from typing import Tuple


class Audio():
  def __init__(self, sr, target_sr, audio_clip,n_fft=2048, hop_length=64, n_mels=32):
    self.sr = sr
    self.target_sr = target_sr
    self.n_fft = n_fft
    self.hop_length = hop_length
    self.n_mels = n_mels
    self.samples = self._process_audio(audio_clip)
    self.fingerprints = self._fingerprint()

  
  def _get_energy_spec(self,spec):
    # Transpose 'spec' upfront and get the shifted versions for calculations
    specT = spec.T
    specT_shifted_vertically = np.roll(specT, shift=-1, axis=0)
    specT_shifted_horizontally = np.roll(specT, shift=-1, axis=1)

    # Calculate the differences for current and previous rows
    diff_current = specT - specT_shifted_horizontally
    diff_previous = specT_shifted_vertically - np.roll(specT_shifted_horizontally, shift=-1, axis=0)

    # Compute the energy_spec matrix using NumPy's greater function for element-wise comparison
    energy_spec = np.greater(diff_current - diff_previous, 0).astype(int)
    return energy_spec.T
  
  def _process_audio(self,audio_clip):
    audio_clip = librosa.to_mono(audio_clip.T)
    audio_clip = audio_clip.reshape(1, -1)
    audio_clip = librosa.resample(audio_clip, orig_sr=self.sr, target_sr=self.target_sr)
    return audio_clip
  def _fingerprint(self):
    fingerprint = []
    spec = librosa.feature.melspectrogram(y=self.samples, sr=self.target_sr, n_fft=self.n_fft, hop_length=self.hop_length, n_mels=self.n_mels)
    energy_spec = self._get_energy_spec(spec)
    for i in range(0,energy_spec.shape[1],128):
      fingerprint.append(energy_spec[:,i:i+128].flatten())
    return fingerprint
    
    
    
class Video():
  def __init__(self, clip):
    self.clip = clip
    self.fingerprints = self._fingerprint()
    
  def _get_top_wavelet(self, frame, top=200):
    coeffs2 = pywt.dwt2(frame, 'haar')
    LL, (LH, HL, HH) = coeffs2
    LL = np.where(LL >= np.sort(LL.flatten())[-top], 1, 0)
    LH = np.where(LH >= np.sort(LH.flatten())[-top], 1, 0)
    HL = np.where(HL >= np.sort(HL.flatten())[-top], 1, 0)
    HH = np.where(HH >= np.sort(HH.flatten())[-top], 1, 0)
    img = LL + LH + HL + HH
    img = np.where(img != 0,1,0)
    return img
    
  def _fingerprint(self):
    fingerprint = []
    i = 0
    supply = 2
    while i < self.clip.duration:
      frame = self.clip.get_frame(i)[:,:,0]
      fingerprint.append(self._get_top_wavelet(frame).flatten())
      i+=supply
    return fingerprint
  
def get_top_wavelet(frame, top=200):
    coeffs2 = pywt.dwt2(frame, 'haar')
    LL, (LH, HL, HH) = coeffs2
    LL = np.where(LL >= np.sort(LL.flatten())[-top], 1, 0)
    LH = np.where(LH >= np.sort(LH.flatten())[-top], 1, 0)
    HL = np.where(HL >= np.sort(HL.flatten())[-top], 1, 0)
    HH = np.where(HH >= np.sort(HH.flatten())[-top], 1, 0)
    img = LL + LH + HL + HH
    img = np.where(img != 0,1,0)
    return img
 
def get_video_fingerprint(clip):
  fingerprint = []
  i = 0
  supply = 2
  while i < clip.duration:
    frame = clip.get_frame(i)[:,:,0]
    fingerprint.append(get_top_wavelet(frame).flatten())
    i+=supply
  return fingerprint

def get_energy_spec(spec):
    # Transpose 'spec' upfront and get the shifted versions for calculations
    specT = spec.T
    specT_shifted_vertically = np.roll(specT, shift=-1, axis=0)
    specT_shifted_horizontally = np.roll(specT, shift=-1, axis=1)

    # Calculate the differences for current and previous rows
    diff_current = specT - specT_shifted_horizontally
    diff_previous = specT_shifted_vertically - np.roll(specT_shifted_horizontally, shift=-1, axis=0)

    # Compute the energy_spec matrix using NumPy's greater function for element-wise comparison
    energy_spec = np.greater(diff_current - diff_previous, 0).astype(int)
    return energy_spec.T
def get_audio_fingerprint(spec):
  fingerprint = []
  energy_spec = get_energy_spec(spec)
  for i in range(0,energy_spec.shape[1],128):
    fingerprint.append(energy_spec[:,i:i+128].flatten())
  return fingerprint 

class Content:
  def __init__(self, name:str, video:Video, audio:Audio):
    self.name = name
    self.video = video
    self.audio = audio



def process_video(name,file_path, frame_size=(256, 144), target_sr=5512,nfft=2048, hop=64)->Tuple[str,list,list,np.ndarray]:
  video_name = os.path.join(file_path, name)
  video_clip = VideoFileClip(video_name,audio=True,target_resolution=(frame_size[0],frame_size[1])).fx(blackwhite) 
  
  audio_clip = video_clip.audio
  sr = audio_clip.fps
  audio_clip = audio_clip.to_soundarray()
  audio_clip = librosa.to_mono(audio_clip.T)
  audio_clip = audio_clip.reshape(1, -1)
  audio_clip = librosa.resample(audio_clip, orig_sr=sr, target_sr=target_sr)
  spec = librosa.feature.melspectrogram(y=audio_clip, sr=target_sr, n_fft=nfft, hop_length=hop, n_mels=32)
  
  video_fingerprint = get_video_fingerprint(video_clip)
  audio_fingerprint = get_audio_fingerprint(spec[0])
  return (name,audio_fingerprint,video_fingerprint,spec[0])

class ContentDataset(Dataset):
    def __init__(self, file_path, cache_into_memory=False):
        self.file_path = file_path
        self.cache_into_memory = cache_into_memory
        self.name_list = self._get_file_names()
        self.content_list = self._init_data(file_path)

    def _get_file_names(self):
        return os.listdir(self.file_path)

    def __getitem__(self, index):
        return self.content_list[index]
    
    def _init_data(self,file_path):
        file_data = [(name, file_path) for name in self.name_list]
        with multiprocessing.Pool(8) as p:
            content_list = p.starmap(process_video, file_data)
        return content_list
    

    def __len__(self):
        return len(self.name_list)