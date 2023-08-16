from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import argparse
from database.db import dbase
from caching.cache import cach
import logging

"""
The file that specifies how selenium interacts with semrush website.

"""

# Argument parser
parser = argparse.ArgumentParser(description="send the username and password")
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('inf') # Loop it till theres no domains or just run once?
args = parser.parse_args()

# Dont use backLinkAnalytics before searching, you cant insert domains at the start there.

delay = 10 # Standard delay

def main():
    w = web()
    w.login()
    # Loop it
    if(args.inf == "yes"):
        while(True):    
            doTheTask(w)
    else:
        doTheTask(w)

def doTheTask(w):
    w.domainOverview()
    w.search()
    w.backLinks()

class web:
    
    """
        Web class that contains all the funcitonality for the program's opertaion. Based on Composition design pattern where parts are built in a separate place - database, redis and linked here
    
    """

    def __init__(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get("https://www.semrush.com/login/")
        self.db = dbase()
        self.redis = cach()
        self.index = 0
        self.domains = []

    def login(self):
        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))

        elem.click()
        elem.send_keys(args.username)

        elem = self.driver.find_element(By.XPATH, "(//input[@id='password'])[1]")
        elem.click()
        elem.send_keys(args.password, Keys.ENTER)

    def domainOverview(self):

        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='srf-report-sidebar-main__link-text'][normalize-space()='Domain Overview'])[1]")))

        elem.click()

    def backLinkAnalytics(self):
        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[normalize-space()='Backlink Analytics'])[1]")))
        elem.click()

        
    def networkGraph(self):
        self.backLinkAnalytics()

        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='___SText_9h10v-yellow-team'][normalize-space()='Network Graph'])[1]")))
        elem.click()

    def backLinks(self):
        self.backLinkAnalytics()
        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='___SText_9h10v-yellow-team'][normalize-space()='Backlinks'])[1]")))
        elem.click()

        # To scroll the visible window down
        self.driver.execute_script("window.scrollTo(0, 1000);")

        export = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='___SInner_5ckir-yellow-team'])[3]")))
        
        # Usual click doesnt work, another way to click
        self.driver.execute_script("arguments[0].click();", export)

        option_csv = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//div[@id='igc-ui-kit-954-option-1'])[1]")))
        self.driver.execute_script("arguments[0].click();", option_csv)

    def organicResearch(self):
        elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='srf-report-sidebar-main__link-text'][normalize-space()='Organic Research'])[1]")))
        elem.click()

    def search(self):
        try:
            elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/input[1]")))
            elem.click()
            d = self.getDomainToProcess()
            elem.send_keys(d["domain"], Keys.ENTER)
            self.setProcessed(d["id"])
        except:
            try:
                elem = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, "(//input[@placeholder='Enter domain, URL or keyword'])[1]")))
                elem.click()
                d = self.getDomainToProcess()
                elem.send_keys(d["domain"], Keys.ENTER)
                self.setProcessed(d["id"])
            except:
                raise

    def setProcessed(self, key):
        self.db.updateWorkDomainsProcessingTrue(key)
    
    def getDomainToProcess(self):
        d = self.getDomain()
        if len(d) != 0:
            while self.redis.checkIfProcessing(d["id"], d["domain"]):
                if len(d) != 0:
                    d = self.getDomain()
                else:
                    print("Done with all!")
                    self.tearDown()
        else:
            print("Done with all!")
            self.tearDown()
        return d

    def getDomain(self):
        if (len(self.domains) == 0 or self.index == len(self.domains)):
            self.domains = self.db.getAllWorkDomains(limit=10)
            
            if len(self.domains) == 0:
                logging.warn("NO DOMAINS TO GET FROM DATABASE")
                self.tearDown()

            self.index = 0
            return self.domains[self.index]           
        else:
            domain = self.domains[self.index]
            self.index += 1
            return domain
        
    def tearDown(self):
        self.driver.quit()


main()