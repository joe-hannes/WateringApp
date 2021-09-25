from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import IntegerRangeField, IntegerField, TelField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

NUMBER_ERROR = 'Please enter a valid number.'
STRING_ERROR = 'Please enter a valid string of characters.'
URI_ERROR = 'Please enter a valid uri string (xxx.xxx.xxx.xxx)'


class SettingsForm(FlaskForm):
    location = StringField(
        'Location',
        validators=[
            Regexp('^([A-z]*)*$', 0, STRING_ERROR)
        ]
    )

    consumption = TelField(
        'Consumption',
         validators=[
             Regexp('^[0-9]*$', 0, message=NUMBER_ERROR)
         ]
     )

    reservoir_size = TelField(
         'Reservoir Size',
         validators=[
             Regexp('^[0-9]*$', 0, message=NUMBER_ERROR)
         ]
     )

    reservoir_warn_level = TelField(
        'Notify when water level is below',
        validators=[
            Regexp('^[0-9]*$',0 , message=NUMBER_ERROR)
        ]
    )

    activation_level = IntegerRangeField('Activate pump below')

    api_key = StringField('API Key')
    submit = SubmitField('Save Settings')

    db_name = StringField(
        'Database name',
        validators=[
            Regexp('^([A-z]*)*$', 0, STRING_ERROR)
        ]
    )

    db_uri = StringField(
        'database uri',
        validators=[
            Regexp('^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})*(([A-z]*\.)*[A-z]*)$',
            0,
            URI_ERROR)
        ]
    )

    db_username = StringField(
        'database username',
        validators=[
            Regexp('^([A-z]*)*$', 0, STRING_ERROR)
        ]
    )

    db_password = StringField('database password',)
