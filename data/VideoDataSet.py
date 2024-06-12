import os
import torch
import pywt
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import cv2

class VideoDataset(Dataset):
    def __init__(self, file_path, cache_into_memory=False):
        self.file_path = file_path
        self.cache_into_memory = cache_into_memory
        self.name_list = self._get_video_names()

    def _get_video_names(self):
        return os.listdir(self.file_path)

    def __getitem__(self, index, frame_size=(256, 144)):
        video_name = self.name_list[index]
        video_cap = cv2.VideoCapture(video_name)
        frames = []
        while True:
            ret, frame = video_cap.read()
            if not ret:
                break
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                transforms.Resize(frame_size),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
                transforms.Grayscale(num_output_channels=1),
            ]) # [F, C, H, W]
            frame = transform(frame)
            frame = self.__haar_transform(frame)
            frames.append(frame)
        video_cap.release()
        video_tensor = torch.tensor(frames)
        return video_tensor
    
    def __haar_transform(self, frame):
        coeffs2 = pywt.dwt2(frame, 'haar')
        LL, (LH, HL, HH) = coeffs2
        return LH + HL

    def __len__(self):
        return len(self.name_list)
    

videos = VideoDataset('compressed_index/')
