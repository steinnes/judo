from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///judotube.db', echo=True)

class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    organization_name = Column(String(64))
    event_type = Column(Enum("Tournament", "Training Camp", "Misc"), default="Tournament")
    continent = Column(String())
    country = Column(String(16))
    city = Column(String())
    start_date = Column(Date)
    end_date = Column(Date)
    min_age = Column(Integer)
    max_age = Column(Integer)
    gender = Column(String())
    description = Column(String())
    attachment = Column(String())
    
    def is_finished(self):
        now = datetime.now()
        return now.date() <= end_date

    def is_going_on(self):
        now = datetime.now()
        return start_date <= now.date() <= end_date

    def __init__(self, name, organization_name, event_type, continent, country, city, start_date, end_date, min_age, max_age, gender, description, attachment):
        self.name = name
        self.organization_name = organization_name
        self.event_type = event_type
        self.continent = continent
        self.country = country
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.description = description
        self.attachment = attachment


engine_c = create_engine('sqlite:///countries.db', echo=True)

class Countries(Base):
    __tablename__ = 'country'
    id = Column(String(2), primary_key=True)
    name = Column(String(64))