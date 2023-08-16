import logging 
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import re


# A regex pattern to identify emails

PATTERN = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

def emailScrapper(domain):

    # sanity the domain
    
    url = domain if domain.startswith("https") else "https://"+ domain

    src = get_page_source(url)
    
    if src != None:
    
        links = get_page_links(src, domain, url)

        if url not in links:
            links.append(url)

        loop = asyncio.get_event_loop()
        found_emails = loop.run_until_complete(get_emails(links))
        return found_emails
    
    else:

        return []


def get_page_source(url):
    
    try:
        page = requests.get(url)
        return page.text
    except Exception as e:
        logging.exception(f"The domain refused connection: {e}")
        return None

def get_page_links(src, domain, url):
    
    links = []
    soup = BeautifulSoup(src, 'html.parser')
    if soup:
        for link in soup.find_all('a'):
            url = link.get('href')
            if domain in str(url) and url.startswith("https"):
                links.append(link.get('href'))

    return list(set(links))

async def get_emails(links):
    
    temp = []
    emails = []
    limit = asyncio.Semaphore(3)
    for link in links:
        task = asyncio.create_task(check(link, limit))
        temp.append(task)
    try:
        await asyncio.gather(*temp)
    except:
        logging.error("Something went wrong with one of async tasks")

    for elem in temp:
        if elem.done():
            emails.extend(elem.result())
    return list(set(emails))

async def check(link, limit):
    
    emails = []
    async with limit:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 200:
                    try:
                        response = requests.get(link)
                        emails2 = re.findall(PATTERN, response.text)
                        for email in emails2:
                            if email not in emails and "/" not in email and "\\" not in email :
                                emails.append(email)
                    except Exception as e:
                        logging.error(f"{link} Didn't Process because: {e}")
                        raise Exception
    return list(set(emails))
