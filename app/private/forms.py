from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField, TextAreaField, StringField
from wtforms.validators import Length


class FileForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=128)])
    description = TextAreaField('Description')
    file = FileField('File', validators=[FileRequired(message='Please select a file.'), FileAllowed(['jpeg', 'jpg', 'png', 'txt', 'doc', 'csv', 'pdf'],
                                                                     'Unsupported file type (supported: JPEG, JPG, PNG, TXT, DOC, CSV, PDF)')])
    submit = SubmitField('Upload')