from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class SettingsForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    consumption = IntegerField('Consumption', validators=[DataRequired()])
    reservoir_size = IntegerField('Reservoir Size', validators=[DataRequired()])
    water_level_warn = IntegerField('Notify when water level is below', validators=[DataRequired()])
    submit = SubmitField('Save Settings')
