from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class TrekForm(FlaskForm):
    title = StringField('Trek Title', validators=[DataRequired(), Length(max=140)])
    location = StringField('Location', validators=[DataRequired(), Length(max=120)])
    difficulty = SelectField('Difficulty', choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')], validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    available_slots = IntegerField('Available Slots', validators=[DataRequired(), NumberRange(min=0)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=255)])
    status = SelectField('Status', choices=[('open', 'Open'), ('closed', 'Closed'), ('completed', 'Completed')], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    assigned_staff = SelectField('Assigned Staff', choices=[], coerce=int, validators=[Optional()])
    submit = SubmitField('Save Trek')
