import time
from collections import OrderedDict

class RamCache:
    """
    یک کش ساده با زمان انقضا (TTL) و ساختار LRU.
    """
    def __init__(self, ttl=300, max_size=100):
        self.ttl = ttl
        self.max_size = max_size
        self.cache = OrderedDict()

    def cache_response(self, user_input, response):
        current_time = time.time()
        if user_input in self.cache:
            self.cache.pop(user_input)
        self.cache[user_input] = (response, current_time)
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def get_cached_response(self, user_input):
        current_time = time.time()
        if user_input in self.cache:
            response, timestamp = self.cache[user_input]
            if current_time - timestamp < self.ttl:
                self.cache.move_to_end(user_input)
                return response
            else:
                self.cache.pop(user_input)
        return None

    def clear(self):
        self.cache.clear()

# ایجاد یک نمونه سراسری
cache_instance = RamCache(ttl=300, max_size=100)
