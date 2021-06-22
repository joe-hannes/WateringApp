from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired

class SettingsForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    consumption = IntegerField('Consumption', validators=[DataRequired()])
    reservoir_size = IntegerField('Reservoir Size', validators=[DataRequired()])
    reservoir_warn_level = IntegerField('Notify when water level is below', validators=[DataRequired()])
    activation_level = IntegerRangeField('Activate pump below')
    submit = SubmitField('Save Settings')
    # TODO: implement reset water_level
    reset_water_level = SubmitField('Reset Water level')
    calculate_refill = SubmitField('Calculate Refill')




class CustomIntegerRangeField(IntegerRangeField):
    """docstring for IntegerRangeField."""

    def __init__(self, validators=None):
        super(IntegerRangeField, self).__init__()
        self.__validator = validator
