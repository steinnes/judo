# encoding=UTF-8

import datetime
import click
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Event, Country, Base

engine = create_engine("sqlite:///judotube.db", echo=False)


def create_session():
    return sessionmaker(bind=engine)()

@click.group()
def cli():
    pass


@cli.command()
def initdb():
    """
    Create the database tables
    """
    Base.metadata.create_all(engine)
    print "Initialized database..."


@cli.command()
def create_test_events():
    """
    Creates two test events, useful for UI testing
    """
    try:
        session = create_session()
        # name, organization_name, event_type, continent,  country, city, start_date, end_date, min_yob, max_yob, gender, description, attachment, location
        event_1 = Event(
            name="reykjavik international",
            organization_name="JFA",
            event_type="Tournament",
            continent="Europe",
            country="Iceland",
            city="reykjavik",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=3),
            min_yob=1955,
            max_yob=2000,
            gender="all",
            description="rock this shit",
            location=u"Ármúla 17a")

        event_2 = Event(
            name="Nordic Open",
            organization_name="JFA",
            event_type="Tournament",
            continent="Europe",
            country="Iceland",
            city="reykjavik",
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=5),
            min_yob=1955,
            max_yob=2000,
            gender="all",
            description="rock this shit",
            location=u"Ármúla 17a")

        session.add_all([event_1,event_2])
        session.commit()
    except sqlalchemy.exc.OperationalError as e:
        print "Exception in `create_test_events`: ", e
        print "\n ... has the database been initialized?"
    else:
        print "Added two test events.."


@cli.command()
def rebuild_countries():
    """
    Rebuilds the countries in the country database table, useful when modifying country list
    """
    session = create_session()
    country_csv = open('data/countries.csv')
    n_countries = 0
    try:
        session.query(Country).delete()  # clear old data
        for line in country_csv.readlines():
            identity, continent, name, capital, iso31662, iso31663, ioc, tld, currency, phone, utc, name_de, capital_de = line.strip().split(";")
            session.add(Country(id=iso31663, continent=continent, name=u'{}'.format(name.decode('utf-8'))))
            n_countries += 1

        session.commit()
    except sqlalchemy.exc.OperationalError as e:
        print "Exception in `rebuild_countries`: ", e
        print "\n ... has the database been initialized?"
    else:
        print "Rebuilt countries, total # of countries: {}".format(n_countries)


@cli.command()
def showsql(table=None):
    """
    Outputs the SQL schema (table structure) as defined in models.py
    """
    def dump(sql, *multiparams, **params):
        print sql.compile(dialect=engine.dialect)
    engine = create_engine("sqlite:///judotube.db", strategy='mock', executor=dump)
    Base.metadata.create_all(engine, checkfirst=False)


@cli.command()
@click.pass_context
def popdb(ctx):
    """
    Populate the database with countries and a couple of test events
    """
    ctx.forward(create_test_events)
    ctx.forward(rebuild_countries)


if __name__ == "__main__":
    cli()
