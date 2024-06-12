import sys
sys.path.append("../")
from libs.Helper.AudioHelper import *
from libs.AudioHash import *
def fingerprint(samples,fanset = 55):
  spec = get_spectrogram(samples,1024,1024)
  peaks_map = compute_constellation_map(spec,5,5,0.01)
  peaks = get_peaks(peaks_map)
  print
  return shazam_hash(peaks, fanset)

def fingerprint_minhash(samples):
  spec = get_spectrogram(samples)
  peaks_map = compute_constellation_map(spec)
  peaks = get_peaks(peaks_map)
  return minhash(peaks)