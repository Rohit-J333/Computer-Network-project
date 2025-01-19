
from constants import *


class LRU:
    cache_dict = {}
    cache = []
    max_chunks = 1
    def __init__(self):
        self.max_chunks = cache_size
    
    def get(self,index):
        # #DEBUG print(f"Cache State is: {self.cache}")
        if index in self.cache:
            self.cache.remove(index)
            self.cache.append(index)
            return self.cache_dict[index]
        else:
            return  ""

    def put(self,index,message):
        
        if index not in self.cache_dict and self.max_chunks != 0:
            if len(self.cache) >= self.max_chunks:
                self.cache_dict.pop(self.cache[0])
                self.cache.pop(0)
            self.cache.append(index)
            self.cache_dict[index] = message
            
        #DEBUG print(f"Cache State is: {self.cache}")
    

            