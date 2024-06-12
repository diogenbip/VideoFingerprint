
import librosa
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
def compute_constellation_map(Y, dist_freq=7, thresh=0.01):
    struct = generate_binary_structure(2, 1)
    neighbors = iterate_structure(struct, dist_freq)
    
    local_max = maximum_filter(Y, footprint=neighbors) == Y
    background = (Y == 0)
    eroded_background = binary_erosion(background, structure=neighbors, border_value=1)
    
    Cmap = local_max ^ eroded_background
    
    return Cmap
  
def get_spectrogram(Y, n_fft = 512, hop_length = 512):
  D = np.abs(librosa.stft(Y[0,:], n_fft=n_fft, hop_length=hop_length))
  S_db = librosa.amplitude_to_db(D, ref=np.max)
  if(S_db.min()<0):
      S_db = S_db - S_db.min()
  return S_db

def get_peaks(peaks):
  peaks = peaks.astype(int)
  peaks = np.transpose(np.nonzero(peaks.T))
  return peaks