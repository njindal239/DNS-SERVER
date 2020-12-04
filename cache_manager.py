import pickle
import os
from time import time
from threading import Lock

"""
Class to manage DNS Cache.

Structure of cache:
- key is composed of domain name and query type
- value is composed of list of answer records, time and ttl

ttl for each entry is used to determine if the cache entry has
expired.
"""
class CacheManager:

    def __init__(self, cacheFileName=None):
        self.cache = {} # This is the shared resource between threads
        self.lock = Lock()

        if cacheFileName is None:
            return

        if os.path.exists(cacheFileName):
            try:
                with open(cacheFileName, "rb") as file:
                    self.cache = pickle.load(file)
            except:
                print("Invalid DNS Cache file")


    """
    Constructs cache key from requested domain name and question
    type.
    """
    def construct_cache_key(self, domain_name, ques_type):
        return f'{domain_name}_{ques_type}'

    """
    Constructs cache value from answer records, and cache time to live
    value and current time.
    """
    def construct_cache_value(self, records, cache_ttl):
        return {'records': records, 'time': time(), 'ttl': cache_ttl}

    """
    Adds a new entry into cache
    """
    def add_cache_entry(self, domain_name, ques_type, records):
        cache_key = self.construct_cache_key(domain_name, ques_type)
        num_records = len(records)
        cache_ttl = records[num_records-1].ttl
        cache_value = self.construct_cache_value(records, cache_ttl)
        
        self.lock.acquire()
        self.cache[cache_key] = cache_value
        self.lock.release()

    """
    Gets cache value for requested domain name and question type,
    if present. If it is present, check if the cache is expired. If
    yes, remove the expired entry. Otherwise, return the cache value.
    """
    def get_cache_entry(self, domain_name, ques_type):
        cache_key = self.construct_cache_key(domain_name, ques_type)
        cache_value = self.cache.get(cache_key)

        # Check if the key does not exist in cache
        if cache_value is None:
            return None

        # Check if the key is expired
        time_diff = time() - cache_value['time']
        cache_ttl = cache_value['ttl']
        if (time_diff > cache_ttl):
            self.lock.acquire()
            del self.cache[cache_key]
            self.lock.release()
            return None

        # Now, we know DNS cache exists and is valid
        return cache_value['records']

    """
    Saves the in-memory cache to persistent file to prevent against
    losing all cache if the server goes down
    """
    def save_to_file(self, cacheFileName):
        try:
            print("Saving DNS Cache")
            with open(cacheFileName, "wb") as file:
                pickle.dump(self.cache, file)
        except:
            print("Failed to save Cached data.")

    """
    Resets the in-mempry cache to default.
    """
    def reset_cache(self):
        self.cache = {}