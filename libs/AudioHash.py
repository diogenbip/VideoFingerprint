import hashlib
import random
def shazam_hash(peaks, fan_value = 15 ):
  IDX_FREQ_I = 0
  IDX_TIME_J = 1
  FINGERPRINT_REDUCTION = 20
  # для каждого пика
  for i in range(peaks.shape[0]):
    for j in range(1,fan_value):
      if i+j < peaks.shape[0]:
        # получим текущее и следующее пиковое значение частоты
        freq1 = peaks[i][IDX_FREQ_I]
        freq2 = peaks[i + j][IDX_FREQ_I]

        # получим текущее и следующее смещение времени пика
        t1 = peaks[i][IDX_TIME_J]
        t2 = peaks[i + j][IDX_TIME_J]

        # получим разницу по времени
        t_delta = t2 - t1

        # если разница между минимум и максимом считаем хэш
        if t_delta >= 0 and t_delta <= 100:
          seq = str(freq1)+"|"+str(freq2)+"|"+str(t_delta)
          h = hashlib.sha1(seq.encode('utf-8'))
          # обрезаем хэш
          yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)
    
def shazam_compare(hashes1, hashes2):
    candidates = set(hashes1) & set(hashes2)
    print(candidates)
    return len(candidates)
    
def minhash(peaks, k=10, n = 32):
  hashfunc = [make_hashfunc() for i in range(n)]
  signatures = []
  peaks = peaks.T
  for i in range(0,peaks.shape[0],k):
    signature = {}
    for h in hashfunc:
      minhash = 0xFFFFFFFF
      data = peaks[i:i+10].flatten()
      for d in data:
        minhash = min(minhash, h(d))
      signature[h] = minhash
    signatures.append(signature)
  
  
  def make_hashfunc():
    # create a random hash function
    a = random.randint(1, 1000)
    b = random.randint(1, 1000)
    p = 2147483647 # a large prime number
    def hashfunc(x):
        return (hash(x) * a + b) % p
    return hashfunc
  return signatures   
          
def hash_function(size):
  seed = random.randint(32, size - 1)
  

  
  def __init__(self,size,max_err):
    self.size = size
    self.max_err = max_err
    self.functions_count = 256
    self.functions = []
    for i in range(self.functions_count):
      self.functions.append(hash_function(self.functions_count))
    
    
  
  def find_min(self,peaks,hash_func):
    min = 0xFFFFFFFF
    peaks = peaks.T
    for i in range(0,peaks.shape[0],10):
      hash = hash_func(peaks[i:i+10,:].flatten())
      if hash < min:
        min = hash
    return min
  
  def signature(self,peaks):
    res = []
    for i in range(self.functions_count):
      res.append(self.find_min(peaks,self.functions[i]))
    return res
  
  def compare(self,signature1,signature2):
    count = 0
    for i in range(self.functions_count):
      if signature1[i] == signature2[i]:
        count += 1
    return count/self.functions_count