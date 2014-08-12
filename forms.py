from wtforms import (
    Form,
    StringField,
    DateField,
    SelectField,
    FileField,
    IntegerField,
    validators
)

from models import EVENT_TYPES, GENDERS


class EventForm(Form):
    name = StringField(u'Event Name', validators=[validators.required()])
    organization_name = StringField(u'Organization Name', validators=[validators.required()])
    event_type = SelectField(u'Event Type', choices=[(i, i) for i in EVENT_TYPES],
        validators=[validators.required()])
    continent = SelectField(u'Continent', validators=[validators.required()])
    country = StringField(u'Country', validators=[validators.required()])
    city = StringField(u'City', validators=[validators.required()])
    start_date = DateField(u'Start Date', validators=[validators.required()])
    end_date = DateField(u'End Date', validators=[validators.required()])
    min_age = IntegerField()
    max_age = IntegerField()
    gender = SelectField(choices=[(i, i) for i in GENDERS],
        validators=[validators.required()])
    description = StringField()
    attachment = FileField()
    address = StringField(u'Address')
    webpage = StringField()
