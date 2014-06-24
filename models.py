from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

EVENT_TYPES = ["Tournament", "Training Camp", "Misc"]
CONTINENTS = ["Europe", "N-America", "S-America", "Africa", "Asia", "Australia"]
GENDERS = ["male", "female", "all"]


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    organization_name = Column(String(64))
    event_type = Column(Enum(*EVENT_TYPES), default="Tournament")
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
    location = Column(String())  # strengur fyrir heimilisfang <-- why not call it address?

    def is_finished(self):
        now = datetime.now()
        return now.date() <= self.end_date

    def is_going_on(self):
        now = datetime.now()
        return self.start_date <= now.date() <= self.end_date

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def update(self, form):
        for k, v in form._fields.iteritems():
            setattr(self, k, v.data)

    @classmethod
    def from_form(cls, form):
        return cls(**dict([(k, v.data) for k, v in form._fields.iteritems()]))


class Country(Base):
    __tablename__ = 'country'
    id = Column(String(3), primary_key=True)
    name = Column(String(64))
    continent = Column(Integer)

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
