"""

A file that I used to just test stuff

"""


# from web.caching.cache import cach
# from web.database.db import dbase

from web.email.emailscrapper import *

# class test:
#     def __init__(self) -> None:
#         self.db = dbase()
#         self.redis = cach()
#         self.index = 0
#         self.domains = []

#     def getDomainToProcess(self):
#         d = self.getDomain()
#         while self.redis.checkIfProcessing(d["id"], d["domain"]):
#             d = self.getDomain()
#         return d

#     def getDomain(self):
#         if (len(self.domains) == 0 or self.index == len(self.domains)):
#             self.domains = self.db.getAllWorkDomains(limit=10)
#             self.index = 0
#             return self.domains[self.index]           
#         else:
#             domain = self.domains[self.index]
#             self.index += 1
#             return domain

# t = test()

# print(type(t.getDomainToProcess()))

# db.eraseWorkDomains()

