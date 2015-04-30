from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField, HiddenField, SelectMultipleField, BooleanField, FileField
from wtforms import widgets
from wtforms.validators import ValidationError
from models import db, User


class RegisterForm(Form):
  name = TextField("",  [validators.Required("Please enter your name.")])
  email = TextField("",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('', [validators.Required("Please enter a password.")])
  submit = SubmitField("")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True


class LoginForm(Form):
  email = TextField("",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('', [validators.Required("Please enter a password.")])
  submit = SubmitField('')
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.password == self.password.data:
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False



class EditProfileForm(Form):
  password = PasswordField('', [])
  name = TextField('', [])
  submit = SubmitField('')
  verify = SubmitField('')
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 

class RequestFriendForm(Form):
  submit = SubmitField("")
  remove = SubmitField("")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AcceptDenyForm(Form):
  accept = SubmitField('Accept')
  deny = SubmitField("Deny")
  hidden = HiddenField("hidden")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    
class CreateCircleForm(Form):
  name = TextField('')
  multiple = SelectMultipleField('', choices=[])
  submit = SubmitField('')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class PostForm(Form):
  textbox = TextAreaField('')
  multiple = SelectMultipleField('', choices=[]) # circles
  files = FileField('')
  submit = SubmitField('')
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class DeleteCircleForm(Form):
  delete = SubmitField('Delete Circle')
  hidden = HiddenField('Hidden')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AddFriendToCircleForm(Form):
  checkbox = SelectMultipleField(
        'Friends',
        choices=[],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
        )
  hidden = HiddenField('Hidden')
  submit = SubmitField("Submit Change")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)


