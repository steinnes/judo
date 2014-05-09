import datetime

import bottle
from bottle import Bottle, HTTPError, run, request, redirect, post, route, static_file
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Event, Countries

Base = declarative_base()
engine = create_engine('sqlite:///judotube.db', echo=True)
create_session = sessionmaker(bind=engine)

engine_c = create_engine('sqlite:///countries.db', echo=True)
country_session = sessionmaker(bind=engine_c)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)


kwargs = {} #global filter variable, using it until I find a better way

# Down here we have the views
@app.route('/')
@bottle.view('index.html')
def index():
    print "index screen"
    kwargs = {}
    session = country_session()
    result = session.query(Countries).all()
    return dict(countries = result, get_url=app.get_url)
    #pass

@app.route('/new', method="GET")
@bottle.view('new.html')
def add_event():
    if request.GET.get("save", "").strip():
    #name, organization_name, event_type, continent,  country, city, start_date, end_date, min_age, max_age, gender, description, attachment
        name = request.GET.get("name", "").strip()
        organization_name = request.GET.get("organization_name", "").strip()
        event_type = request.GET.get("event_type", "").strip()
        continent = request.GET.get("continent", "").strip()
        country = request.GET.get("country", "").strip()
        city = request.GET.get("city", "").strip()
        tempstart_date = request.GET.get("start_date", "").strip("")
        tempstart_date = tempstart_date.split("-")
        print tempstart_date
        start_date = datetime.date(int(tempstart_date[0], 10), int(tempstart_date[1], 10), int(tempstart_date[2], 10))
        tempend_date = request.GET.get("end_date", "").strip("")
        tempend_date = tempend_date.split("-")
        print tempend_date
        end_date = datetime.date(int(tempend_date[0], 10), int(tempend_date[1], 10), int(tempend_date[2], 10))
        min_age = request.GET.get("min_age", "").strip()
        max_age = request.GET.get("max_age", "").strip()
        gender = request.GET.get("gender", "").strip()
        description = request.GET.get("description", "").strip()
        attachment = request.GET.get("attachment", "").strip()

        session = create_session()
        new_task = Event(name, organization_name, event_type,continent,  country, city, start_date, end_date, min_age, max_age, gender, description, attachment)
        session.add(new_task)
        session.commit()
 
        redirect("/")

    session = country_session()
    result = session.query(Countries).all()
    return dict(countries = result)

@post('/events')
@app.route('/events')
@bottle.view('events.html')
def events():
    kwargs = {}
    myDict = request.query.decode()
    if myDict['countries'] != 'Any':
        kwargs['country'] = myDict['countries']
    if myDict['continents'] != 'Any':
        kwargs['continent'] = myDict['continents']
    session = create_session()
    result = session.query(Event)
    for attr, value in kwargs.items():
        result = result.filter(getattr(Event, attr).like("%%%s%%" % value))
    #myResultList = [(item.id, item.country, item.name, item.start_date, item.organization_name) for item in result]
    print result
    return dict(events=result, get_url=app.get_url)

@app.route('/events/<current:int>')
@bottle.view('event.html')
def event(current):
    print current
    print type(current) is int
    session = create_session()
    result = session.query(Event).filter_by(id = current)
    print result
    return dict(event = result, get_url = app.get_url)


@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
app.run(host='localhost', port=8080, debug=True, reloader=True)
