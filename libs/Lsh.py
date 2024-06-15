import numpy as np
import random

class MinHash:
  def __init__(self, num_perm):
    self.permutations = self._permutations_generate(num_perm)
  
  def _permutations_generate(self, num_perm)->list:
    permutations = []
    count = 0
    while count < num_perm:
      perm = random.sample(range(0, 255), 100)
      permutations.append(perm)
      count += 1
    return permutations
      
  def hash(self,array)->list:
    signature = []
    for permutation in self.permutations:
      for j in permutation:
        if(array[j] == 1):
          signature.append(j)
          break
    return signature
  
  def jaccard_similarity(self,signature1, signature2):
    intersection = np.sum(np.bitwise_and(signature1, signature2))
    union = np.sum(np.bitwise_or(signature1, signature2))
    return intersection / union 

class LSH:
    def __init__(self, threshold:float,num_hash_functions:int = 100,bands:int = 25, rows:int = 4):
      assert threshold > 0 and threshold < 1
      assert bands*rows == num_hash_functions
      self._threshold = threshold
      self._num_hash_functions = num_hash_functions
      self._bands = bands
      self._rows = rows
      self._min_hash = MinHash(num_hash_functions)
      self._buckets = {}
    
    def clear(self):
      self._buckets.clear()

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
        if add_to_bucket:
          for i in range(self._bands):
            if band_hashes[i] not in self._buckets:
              self._buckets[band_hashes[i]] = []
            self._buckets[band_hashes[i]].append((min_hashes, name, time))
          
    def _compute_band_hash(self, min_hashes: list, i: int) -> str:
        """Compute a hash for quick bucket match search."""
        band_hash_list = []
        for j in range(self._rows):
            # Adding the rows corresponding to ith band
            band_hash_list.append('%02d' % min_hashes[i * self._rows + j])

        # Adding the number i to distinguish between bands
        band_hash_list.append('%02d' % i)
        return ''.join(band_hash_list)
      
    def get_min_hash(self):
      return self._min_hash
      