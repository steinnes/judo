#coding=UTF-8
import datetime
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
engine = create_engine("sqlite:///judotube.db", echo=True)
 
########################################################################
class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
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
    gender = Column(String(30))
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
        self.continent = continent
        self.event_type = event_type
        self.country = country
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.description = description
        self.attachment = attachment
 
#----------------------------------------------------------------------
def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    #name, organization_name, event_type, continent,  country, city, start_date, end_date, min_age, max_age, gender, description, attachment
    session.add_all([
        Event("reykjavik international", "JFA", "Tournament", "Europe", "Iceland", "reykjavik", datetime.date(2014, 05, 10), datetime.date(2014, 05, 13), 15, 60, "all", "rock this shit", ""),
        Event("Nordic Open", "JFA", "Tournament",  "Europe", "Iceland", "reykjavik", datetime.date(2014, 06, 10), datetime.date(2014, 05, 13), 15, 60, "all", "rock this shit", "")
        ])
    session.commit()
 
if __name__ == "__main__":
    main()