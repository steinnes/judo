import bottle
from datetime import datetime, date
from bottle import request, redirect, post, static_file, template
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Event, Country, CONTINENTS, EVENT_TYPES, GENDERS

from forms import EventForm

Base = declarative_base()
engine = create_engine('sqlite:///judotube.db', echo=True)
create_session = sessionmaker(bind=engine)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine,  # SQLAlchemy engine created with create_engine function.
    Base.metadata,  # SQLAlchemy metadata, required only if create=True.
    keyword='db',  # Keyword used to inject session database in a route (default 'db').
    create=True,  # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True,  # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False  # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)


# Down here we have the views
@app.route('/')
@bottle.view('index.html')
def index():
    #Get countries and print them into the select box
    session = create_session()
    result = session.query(Country).all()

    #Let's also get upcoming tournaments
    matching_events = session.query(Event).\
                        filter(Event.end_date > datetime.now()).\
                        order_by(Event.start_date).\
                        limit(10)
    e = list(matching_events)

    return dict(countries=result,
                continents=CONTINENTS,
                events=e,
                year = date.today().year,
                get_url=app.get_url)


@app.route('/new', method="POST")
def add_event():
    def _dup(l):
        return [(i, i) for i in l]

    session = create_session()
    form = EventForm(request.forms)
    form.continent.choices = _dup(CONTINENTS)
    countries = session.query(Country)
    #form.country.choices = [(c.id, c.name) for c in countries.all()]
    #form.gender.choices = _dup(["male", "female", "all"])

    if form.validate():
        session = create_session()
        new_task = Event.from_form(form)
        session.add(new_task)
        session.commit()
        redirect("/")
    else:
        print "gender=", form.gender
        print dict(request.forms)
        print form.errors
        print type(form.errors)
        return new(errors=form.errors)


@app.route('/new', method="GET")
@bottle.view('new.html')
def new(errors=None):
    session = create_session()

    return dict(
        countries=session.query(Country).all(),
        continents=CONTINENTS,
        eventtypes=EVENT_TYPES,
        genders=GENDERS,
        errors=errors,
        get_url=app.get_url)


@post('/events')
@app.route('/events')
@bottle.view('events.html')
def events():
    form = request.query.decode('utf-8')
    # XXX: make WTForm for this and validate!


    filters = {}
    if form['countries'] != 'Any':
        filters['country'] = form['countries']
    if form['continents'] != 'Any':
        filters['continent'] = CONTINENTS[int(form['continents'])]
    del form['countries']
    del form['continents']

    session = create_session()
    matching_events = session.query(Event).filter_by(**filters).\
                        filter(Event.end_date > datetime.now()).\
                        filter(Event.start_date >= datetime.now()).\
                        order_by(Event.start_date)

    if form['age']:
        matching_events = matching_events.\
                            filter(form['age'] <= Event.max_age).\
                            filter(form['age'] >= Event.min_age)

    e = list(matching_events)
    return dict(events=e, get_url=app.get_url)


@app.route('/events/<current:int>')
@bottle.view('event.html')
def event(current):
    print current
    print type(current) is int
    session = create_session()
    result = session.query(Event).get(current)
    #result = session.query(Event).filter_by(id=current)
    print result
    return dict(event=result, get_url=app.get_url)


@app.route('/admin')
@bottle.view('admin.html')
def admin():
    session = create_session()
    matching_events = session.query(Event).order_by(Event.start_date)

    e = list(matching_events)
    return dict(events=e, get_url=app.get_url)


@app.route('/delete/<id:int>')
def delete(id):
    session = create_session()
    event = session.query(Event).get(id)
    session.delete(event)
    session.commit()
    redirect("/admin")

@app.route('/edit/<id:int>')
@bottle.view('edit.html')
def edit(id, errors=None):
    session = create_session()
    e = session.query(Event).get(id)

    return dict(countries=session.query(Country).all(),
                continents=CONTINENTS,
                eventtypes=EVENT_TYPES,
                genders=GENDERS,
                errors=errors,
                event=e,
                get_url=app.get_url)

@app.route('/edit/<id:int>', method="POST")
def edit_event(id):
    def _dup(l):
        return [(i, i) for i in l]

    session = create_session()
    form = EventForm(request.forms)
    form.continent.choices = _dup(CONTINENTS)
    countries = session.query(Country)

    if form.validate():
        session = create_session()
        eventToEdit = session.query(Event).get(id)
        eventToEdit.update(form)
        session.commit()
        redirect("/admin")
    else:
        print "gender=", form.gender
        print dict(request.forms)
        print form.errors
        print type(form.errors)
        return new(errors=form.errors)

@app.route('/about')
@bottle.view('about.html')
def about():
    return dict(get_url=app.get_url)

@app.route('/contact')
@bottle.view('contact.html')
def contact():
    return dict(get_url=app.get_url)

@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

app.run(host='localhost', port=8080, debug=True, reloader=True)
