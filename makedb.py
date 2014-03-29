#coding=UTF-8
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Event, Base
 
engine = create_engine("sqlite:///judotube.db", echo=True)

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
