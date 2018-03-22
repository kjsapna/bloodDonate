from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256

class PeopleProfile(db.Model):
  __tablename__ = 'tbl_people_profile'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  # lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120))
  phone = db.Column(db.Integer)
  address= db.Column(db.String(100))
  bloodCategoryId = db.Column(db.String(100))
  active = db.Column(db.Boolean, default = False)


  def __init__(self, name, email, password, phone, address, bloodCategoryId):
    self.name = name
    self.email = email
    self.password = password
    self.phone = phone
    self.address = address
    self.bloodCategoryId = bloodCategoryId

  def hash_password(self, password):
    self.password = pbkdf2_sha256.hash(password)
    # return self.password

  def verify_password(self, password):
    return pbkdf2_sha256.verify(password, self.password)
    # hash = pbkdf2_sha256.verify(password, self.password)
    #
    # if self.password == hash:
    #     print True
    # else:
    #     print False
