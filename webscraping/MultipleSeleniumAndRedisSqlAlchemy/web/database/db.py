import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy import exc
import logging
from urllib.parse import urlparse


"""

used sqlalchemy ORM here to define database operations.

"""

# ORM class inheritance
Base = declarative_base()

class dbase:

    def __init__(self) -> None:

        """
            
            Create models and bind database engine
        
        """

        self.engine= sqlalchemy.create_engine("mysql://root:12345@localhost:3306/scraper")
        Base.metadata.create_all(bind=self.engine)
        
    def addToWorkDomains(self, domain) -> None:

        """
        
            Extract root domain from a given url and then insert it
        
        """

        
        url = urlparse(domain).netloc()
        
        w = workDomains(domain=url)

        with self.getSession() as session:
            session.add(w)

    def getAllWorkDomains(self, limit = 100) -> []:


        """
        
            Get list of domains that aren't processed
        
        """

        domains = []
        with self.getSession() as session:
            for domain in session.query(workDomains).filter(workDomains.processed == "no").limit(limit):
                domains.append({"id": domain.id, "domain": domain.domain})
        return domains

    def addToEmailFoundDomains(self, domain, email) -> None:
        
        url = urlparse(domain).netloc()
        
        w = emailFoundDomains(domain = url, email = email)
        with self.getSession() as session:
            session.add(w)

    def getAllEmailFoundDomains(self, limit = 100) -> []:
        domains = []
        with self.getSession() as session:
            for domain in session.query(emailFoundDomains).limit(limit):
                domains.append({"id": domain.id, "domain": domain.domain, "email": domain.email})
        return domains
    
    def eraseWorkDomains(self) -> None:
        with self.getSession() as session:
            session.query(workDomains).delete()

    def eraseEmailFoundDomains(self) -> None:
        with self.getSession() as session:
            session.query(emailFoundDomains).delete()

    def deleteWorkDomain(self, index) -> None:
        with self.getSession() as session:
            session.query(workDomains).filter(workDomains.id == index).delete()
    
    def deleteEmailfoundDomain(self, index) -> None:
        with self.getSession() as session:
            session.query(emailFoundDomains).filter(emailFoundDomains.id == index).delete()
    
    def updateWorkDomainsProcessingTrue(self, index) -> None:
        with self.getSession() as session:
            session.query(workDomains).filter(workDomains.id == index).update({"processed": "yes"})
    


    """
        A context manager is important to enable exception free database transaction. A session can only do one operation (block defined under "with") and if you call a different block under "with" then you get an error. To prevent it you have to make a new session everytime.
    
    """

    @contextmanager
    def getSession(self):
        session = Session(bind=self.engine)
        try:
            yield session
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            logging.warning("Duplicate")
        except:
            session.rollback()
            logging.critical("Unknown error")
        finally:
            session.close()


"""

Models to work with the database tables

"""


class workDomains(Base):

    __tablename__ = 'work_domains'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    domain = Column(String(100), unique= True)

    processed = Column(String(10), default="no")

class emailFoundDomains(Base):
    
    __tablename__ = 'emailFoundDomains'

    id = Column(Integer, primary_key=True, autoincrement=True)

    domain = Column(String(100), unique= True)

    email = Column(String(1000))
