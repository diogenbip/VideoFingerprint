import os
from torch.utils.data import Dataset
from moviepy.video.io.VideoFileClip import VideoFileClip
import librosa


class AudioDataset(Dataset):
    def __init__(self, file_path, cache_into_memory=False,target_sr=5512):
        self.file_path = file_path
        self.cache_into_memory = cache_into_memory
        self.target_sr = target_sr
        self.name_list = self._get_video_names()

    def _get_video_names(self):
        return os.listdir(self.file_path)

    def __getitem__(self, index):
        video_name = os.path.join(self.file_path, self.name_list[index])
        video_clip = VideoFileClip(video_name)
        audio_clip = video_clip.audio
        sr = audio_clip.fps
        audio_clip = audio_clip.to_soundarray()
        audio_clip = librosa.to_mono(audio_clip.T)
        audio_clip = audio_clip.reshape(1, -1)
        audio_clip = librosa.resample(audio_clip, orig_sr=sr, target_sr=self.target_sr)
        return audio_clip
    

    def __len__(self):
        return len(self.name_list)
