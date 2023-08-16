# Parallel selenium

This project signifies how I used asyncio subprocess, redis database and sqlalchemy to make a functional semrush bot.


# Notes

## Redis

Its a type of database that is used to remove duplicates in a queue, allowing collaboration between multiple multi-threaded processes. The database is stored in the RAM, which means its fast.

# References

## Asyncio

https://superfastpython.com/asyncio-subprocess/

## Redis

https://realpython.com/python-redis/
https://redis.io/docs/getting-started/installation/install-redis-on-windows/

You might have to do 
`sudo systemctl restart redis-server` 
to ensure your redis service is reachable.