import pickle
import os
from time import time

"""
Structure of cache:
- key is composed of domain name and query type
- value is composed of list of answer records and time
"""
class CacheManager:
    DEFAULT_CACHE_HOURS = 3

    def __init__(self, cacheFileName=None, cacheHours=DEFAULT_CACHE_HOURS):
        self.cacheHours = cacheHours
        self.cache = {}

        if cacheFileName is None:
            return

        if os.path.exists(cacheFileName):
            try:
                with open(cacheFileName, "rb") as file:
                    self.cache = pickle.load(file)
            except:
                print("Invalid DNS Cache file")


    def construct_cache_key(self, domain_name, ques_type):
        return f'{domain_name}_{ques_type}'

    def construct_cache_value(self, records):
        return {'records': records, 'time': time()}


    def add_cache_entry(self, domain_name, ques_type, records):
        cache_key = self.construct_cache_key(domain_name, ques_type)
        cache_value = self.construct_cache_value(records)
        self.cache[cache_key] = cache_value

    def get_cache_entry(self, domain_name, ques_type):
        cache_key = self.construct_cache_key(domain_name, ques_type)
        cache_value = self.cache.get(cache_key)

        # Check if the key does not exist in cache
        if cache_value is None:
            return None

        # Check if the key is expired
        time_diff = time() - cache_value['time']
        if (time_diff > self.cacheHours*3600):
            del self.cache[cache_key]
            return None

        # Now, we know DNS cache exists and is valid
        return cache_value['records']

    def save_to_file(self, cacheFileName):
        try:
            print("Saving DNS Cache")
            with open(cacheFileName, "wb") as file:
                pickle.dump(self.cache, file)
        except:
            print("Failed to save Cached data.")

    def reset_cache(self):
        self.cache = {}