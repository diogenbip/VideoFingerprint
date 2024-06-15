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

class Audio():
  def __init__(self, sr, samples):
    self.sr = sr
    self.samples = samples
class Video():
  def __init__(self, clip, fps,duration):
    self.clip = clip
    self.fps = fps
    self.duration = duration
    
  def _get_top_wavelet(self, frame, top=200):
    coeffs2 = pywt.dwt2(self.clip.get_frame(frame)[:,:,0], 'haar')
    LL, (LH, HL, HH) = coeffs2
    LL = np.where(LL >= np.sort(LL.flatten())[-top], 1, 0)
    LH = np.where(LH >= np.sort(LH.flatten())[-top], 1, 0)
    HL = np.where(HL >= np.sort(HL.flatten())[-top], 1, 0)
    HH = np.where(HH >= np.sort(HH.flatten())[-top], 1, 0)
    img = LL + LH + HL + HH
    img = np.where(img != 0,1,0)
    return img
    
  def fingerprint(self, frame, top=200):
    return self._get_top_wavelet(frame, top)
    

class Content:
  def __init__(self, name:str, video:Video, audio:Audio):
    self.name = name
    self.video = None
    self.audio = None

class ContentDataset(Dataset):
    def __init__(self, file_path, cache_into_memory=False):
        self.file_path = file_path
        self.cache_into_memory = cache_into_memory
        self.name_list = self._get_file_names()
        self.content_list = self._init_data()

    def _get_file_names(self):
        return os.listdir(self.file_path)

    def __getitem__(self, index):
        return self.content_list[index]
      
    def process_video(self,name, file_path, frame_size, target_sr):
      video_name = os.path.join(file_path, name)
      video_clip = VideoFileClip(video_name).fx(blackwhite).resize(frame_size)
      video = Video(video_clip, video_clip.fps, video_clip.duration)
      
      audio_clip = video_clip.audio
      sr = audio_clip.fps
      audio_clip = audio_clip.to_soundarray()
      audio_clip = librosa.to_mono(audio_clip.T)
      audio_clip = audio_clip.reshape(1, -1)
      audio_clip = librosa.resample(audio_clip, orig_sr=sr, target_sr=target_sr)
      audio = Audio(target_sr, audio_clip)
      content = Content(name, video, audio)
      return content
    
    def _init_data(self, frame_size=(256, 144),target_sr=5512):
        with multiprocessing.Pool(8) as p:
            content_list = p.starmap(self.process_video, [(name, self.file_path, frame_size, target_sr) for name in tqdm(self.name_list)])
        return content_list

    

    def __len__(self):
        return len(self.name_list)