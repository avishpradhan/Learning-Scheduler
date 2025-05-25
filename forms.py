from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    days_left = IntegerField('Days Until Exam', validators=[DataRequired(), NumberRange(min=1)])
    total_units = IntegerField('Total Units', validators=[DataRequired(), NumberRange(min=1)])
    
    priority = SelectField(
        'Priority',
        choices=[('1', 'Highest'), ('2', 'High'), ('3', 'Medium'), ('4', 'Low'), ('5', 'Lowest')],
        validators=[DataRequired()]
    )
    
    complexity = SelectField(
        'Complexity',
        choices=[('1', 'Very Easy'), ('2', 'Easy'), ('3', 'Medium'), ('4', 'Hard'), ('5', 'Very Hard')],
        validators=[DataRequired()]
    )
    
    stress_level = SelectField(
        'Stress Level',
        choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High'), ('5', 'Very High')],
        validators=[DataRequired()]
    )
    
    fatigue_level = SelectField(
        'Fatigue Level',
        choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High'), ('5', 'Very High')],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Add Subject')
    
