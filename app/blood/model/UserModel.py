from .. import db

class User(db.Model):
  __tablename__ = 'tbl_user'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100))
  # lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  password= db.Column(db.String(54))
  phone = db.Column(db.Integer)
  def __init__(self, username, email, password, phone):
    self.username = username.title()
    # self.lastname = lastname.title()
    self.email = email.lower()
    self.password = password.title()
    self.phone=phone.title()


  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
    # if(self.password==password):
    #   return True
    # else:
    #   return false
