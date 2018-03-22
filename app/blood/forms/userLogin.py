from flask_wtf import Form
from ..model import  PeopleProfile as p

from wtforms import TextField, BooleanField,SubmitField,  PasswordField ,ValidationError,validators
from wtforms.validators import Required
from .. import db


class log(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Login")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    userl = p.query.filter_by(email = self.email.data.lower()).first()
    if userl and userl.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
