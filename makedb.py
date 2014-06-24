#encoding=UTF-8
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Event, Country, Base

engine = create_engine("sqlite:///judotube.db", echo=True)


def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    #name, organization_name, event_type, continent,  country, city, start_date, end_date, min_age, max_age, gender, description, attachment, location
    event_1 = Event(name="reykjavik international", organization_name="JFA", event_type="Tournament", continent="Europe", country="Iceland", city="reykjavik", start_date=datetime.date(2014, 05, 10), end_date=datetime.date(2014, 05, 13), min_age=15, max_age=60, gender="all", description="rock this shit", location="Ármúla 17a")
    event_2 = Event(name="Nordic Open", organization_name="JFA", event_type="Tournament", continent="Europe", country="Iceland", city="reykjavik", start_date=datetime.date(2014, 06, 10), end_date=datetime.date(2014, 05, 13), min_date=15, max_date=60, gender="all", description="rock this shit", location="Ármúla 17a")
    session.add_all([event_1, event_2])

    country_csv = open('data/countries.csv')
    for line in country_csv.readlines():
        identity, continent, name, capital, iso31662, iso31663, ioc, tld, currency, phone, utc, name_de, capital_de = line.strip().split(";")
        session.add(Country(id=iso31663, continent=continent, name=u'{}'.format(name.decode('utf-8'))))

    session.commit()


if __name__ == "__main__":
    main()
