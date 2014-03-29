import datetime

import bottle
from bottle import HTTPError, run, request
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///judotube.db', echo=True)
create_session = sessionmaker(bind=engine)

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

# Down here we have the views
@app.route('/')
@bottle.view('index.html')

def index():
    return dict()
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

@app.route('/events')
@bottle.view('events.html')
def events():
    session = create_session()
    result = session.query(Event).all()
    #myResultList = [(item.id, item.country, item.name, item.start_date, item.organization_name) for item in result]
   # print myResultList[0]
    return dict(events=result)
    
app.run(host='localhost', port=8080, debug=True, reloader=True)
