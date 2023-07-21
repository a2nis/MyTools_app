from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import InputRequired, Regexp, NumberRange

class GroupForm(FlaskForm):
  no_socio = IntegerField('Nro. Socio', validators=[InputRequired(), NumberRange(min=1, message='Mayor a 1')])
  group = TextAreaField('Groups', validators=[InputRequired(), Regexp(r'^(?:[0-9]{2}|[A-Z]{2}|[A-Z][0-9]),(?:[0-9]{2}|[A-Z]{2}|[A-Z][0-9])(?:,(?:[0-9]{2}|[A-Z]{2}|[A-Z][0-9]))*$', message='Formato incorrecto')])
