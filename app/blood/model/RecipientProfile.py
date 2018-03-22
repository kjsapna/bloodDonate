from .. import db
class RecipientProfile(db.Model):
  __tablename__ = 'tbl_recipient'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  people_profile_id = db.Column(db.String(100))
  # lastname = db.Column(db.String(100))
  phone = db.Column(db.Integer)
  email = db.Column(db.String(120), unique=True)
  address= db.Column(db.String(100))
  bloodCategoryId = db.Column(db.String(10))

  # password= db.Column(db.String(54))

  def __init__(self,people_profile_id, name, phone, email, address,bloodCategoryId):
    self.name = name
    self.people_profile_id = people_profile_id
    # self.lastname = lastname.title()
    # self.password = password.title()
    self.phone = phone
    self.email = email
    self.address = address
    self.bloodCategoryId = bloodCategoryId
