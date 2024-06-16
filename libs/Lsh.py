import numpy as np
import hashlib
from models.audio.AudioHashModel import AudioHash
import scipy.stats as stats

class MinHash:
  def __init__(self, num_perm, seed=333):
    self.permutations = self._permutations_generate(num_perm, seed)
  
  def _permutations_generate(self, num_perm, seed=333)->list:
    np.random.seed(seed)
    permutations = []
    for _ in range(num_perm):
      res = np.random.choice( 255, 100,replace=False)
      while stats.entropy(res) < 4.47:
        res = np.random.choice( 255, 100,replace=False)
      permutations.append(res) 
    return permutations
      
  def hash(self,array)->list:
    signature = []
    for permutation in self.permutations:
      for j in permutation:
        if(array[j] > 0):
          signature.append(j)
          break
    return signature
  
  def jaccard_similarity(self,signature1, signature2):
    intersection = np.sum(np.bitwise_and(signature1, signature2))
    union = np.sum(np.bitwise_or(signature1, signature2))
    return intersection / union 

class LSH:
    def __init__(self, threshold:float,seed:int = 3267,num_hash_functions:int = 100,bands:int = 25, rows:int = 4):
      assert threshold > 0 and threshold < 1
      assert bands*rows == num_hash_functions
      self._threshold = threshold
      self._num_hash_functions = num_hash_functions
      self._bands = bands
      self._rows = rows
      self._min_hash = MinHash(num_hash_functions, seed)
      self._buckets = {}
    
    def clear(self):
      self._buckets.clear()

    def searchFingerprints(self, fingerprints):
      compared_sketches = set()
      #N x 32 x 128
      for i,fs in enumerate(fingerprints):
        for j,f in enumerate(fs):
          for key,bucket in self._buckets.items():
            k = ''.join(map(str, f))
            if k  in bucket and k + key not in compared_sketches:
              compared_sketches.add(k+key)
              for sims in bucket[k]:
                if len(sims[0]) == len(fs):
                  jac = self._min_hash.jaccard_similarity(sims[0], fs)
                  if jac >= self._threshold:print((key,( sims[1] * (128*64/5512))/60,((i+j)*(128*64/5512))/60, jac)) 
            
      
    def addFingerprints(self, fingerprints,name):
        mapper = {}
        #N x 32 x 128
        for i,fs in enumerate(fingerprints):
          for j,f in enumerate(fs):
            key = ''.join(map(str, f))
            if key not in mapper:
              mapper[key] = []
            mapper[key].append((fs,i,j))
        
        self._buckets[name] = mapper
              
          
    
    def searchInDb(self, fingerprints,audioHashes:AudioHash,name,time):
        min_hashes = self._min_hash.hash(fingerprints)
        band_hashes = []
        compared_sketches = set()
        
        if(len(min_hashes) != self._num_hash_functions):
          return None
        
        
        for i in range(self._bands):
          band_hashes.append(self._compute_band_hash(min_hashes, i))
        dbHashes = audioHashes.getMinHash(tuple(band_hashes))
        
        for dbHashTuple in dbHashes:
          if dbHashTuple[0] in compared_sketches:
            continue
          dbHash = list(map(int, dbHashTuple[1].split(",")))
          jac = self._min_hash.jaccard_similarity(dbHash, min_hashes)
          if jac >= self._threshold:
            return (time, dbHashTuple[0], dbHashTuple[2], dbHashTuple[3], jac)
          compared_sketches.add(dbHashTuple[0])
          
    def search(self, fingerprints,name,time, add_to_bucket = True)->tuple :
        min_hashes = self._min_hash.hash(fingerprints)
        band_hashes = []
        compared_sketches = set()
        
        if(len(min_hashes) != self._num_hash_functions):
          return None
        
        
        for i in range(self._bands):
          band_hashes.append(self._compute_band_hash(min_hashes, i))
          if band_hashes[i] in self._buckets:
            for sketch_to_check in self._buckets[band_hashes[i]]:
              check_key = ''.join(str(x) for x in sketch_to_check)
              if check_key not in compared_sketches:
                jac = self._min_hash.jaccard_similarity(sketch_to_check[0], min_hashes)
                if jac >= self._threshold:
                  return (sketch_to_check[0],sketch_to_check[1],sketch_to_check[2], jac)
                compared_sketches.add(check_key)
                
        if add_to_bucket and len(min_hashes) == self._num_hash_functions:
          for i in range(self._bands):
            if band_hashes[i] not in self._buckets:
              self._buckets[band_hashes[i]] = []
            self._buckets[band_hashes[i]].append((min_hashes, name, time))
            
    def add(self, fingerprints, name, time):
        min_hashes = self._min_hash.hash(fingerprints)
        band_hashes = []
        if(len(min_hashes) != self._num_hash_functions):
          return None
        
        for i in range(self._bands):
          band_hashes.append(self._compute_band_hash(min_hashes, i))
          if band_hashes[i] not in self._buckets:
            self._buckets[band_hashes[i]] = []
          self._buckets[band_hashes[i]].append((min_hashes, name, time))
          
    def _compute_band_hash(self, min_hashes: list, i: int) -> str:
        """Compute a hash for quick bucket match search."""
        band_hash_list = []
        for j in range(self._rows):
            # Adding the rows corresponding to ith band
            band_hash_list.append(str(min_hashes[i * self._rows + j]))
        return hashlib.md5(''.join(band_hash_list).encode('utf-8')).hexdigest()


    def get_min_hash(self):
      return self._min_hash
      