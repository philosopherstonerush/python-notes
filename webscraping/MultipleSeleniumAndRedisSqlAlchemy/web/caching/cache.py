import redis

class cach:

    def __init__(self):
        self.r = redis.Redis()
        # remove existing entries in the RAM
        self.r.flushdb()

    # key is the id in the database
    def checkIfProcessing(self, key, domain):
        # Check if the key exists in the database
        if (self.r.exists(key)):
            return True
        else:
            # set add operation
            self.r.sadd(key, domain)
            return False