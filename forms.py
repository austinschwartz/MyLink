from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField, HiddenField, SelectMultipleField
from wtforms.validators import ValidationError
from models import db, User


class RegisterForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
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
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Log In")
   
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
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Update Account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 

class RequestFriendForm(Form):
  submit = SubmitField("Add Friend")
  remove = SubmitField("Remove Friend")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AcceptDenyForm(Form):
  accept = SubmitField('Accept')
  deny = SubmitField("Deny")
  hidden = HiddenField("hidden")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    
class CreateCircleForm(Form):
  name = TextField("Circle Name")
  multiple = SelectMultipleField(u'Friends', choices=[])
  submit = SubmitField('Create Circle')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
