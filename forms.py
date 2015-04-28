from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField, HiddenField
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
  password = PasswordField('', [validators.Required("Please enter a password.")])
  submit = SubmitField('')
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 

class RequestFriendForm(Form):
  submit = SubmitField("Add Friend")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)


class AcceptDenyForm(Form):
  accept = SubmitField('Accept')
  deny = SubmitField("Deny")
  hidden = HiddenField("hidden")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    

