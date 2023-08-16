"""

The thing that I am proud of is the fact that I was able to make selenium run parallely at the same time and learnt sqlalchemy ORM and redis de-duplication.

"""


import asyncio
from web.email.emailscrapper import *

async def main():
    
    # You can create as many processes as you want but make sure to set it process.wait at the end.

    process1 = await asyncio.create_subprocess_shell('python web\web.py <user> <password> no')
    process2 = await asyncio.create_subprocess_shell("python web\web.py <user> <password> no")
    
    await process1.wait()
    await process2.wait()

asyncio.run(main())