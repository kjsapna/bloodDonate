from .. import db
class DonorProfile(db.Model):
  __tablename__ = 'tbl_donor'
  id = db.Column(db.Integer, primary_key = True)
  donor_name = db.Column(db.String(100))
  # lastname = db.Column(db.String(100))
  people_profile_id = db.Column(db.String(100))
  bloodCategoryId = db.Column(db.Integer)
  donor_phone = db.Column(db.Integer)
  donor_email = db.Column(db.String(120), unique=True)
  donor_address = db.Column(db.String(100))
  donor_age = db.Column(db.Integer)
  donor_gender = db.Column(db.Boolean, default = False)
  # recipeint_name = db.Column(db.String(100))
  # recipient_blood_type = db.Column(db.String(10))

  # password= db.Column(db.String(54))

  def __init__(self, people_profile_id, donor_name, bloodCategoryId, donor_phone, donor_email, donor_address, donor_age, donor_gender ):
    self.donor_name = donor_name
    self.people_profile_id = people_profile_id
    # self.lastname = lastname.title()
    # self.password = password.title()
    self.bloodCategoryId = bloodCategoryId
    self.donor_phone = donor_phone
    self.donor_email = donor_email
    self.donor_address = donor_address
    self.donor_age = donor_age
    self.donor_gender = donor_gender
    # self.recipeint_name = recipeint_name
    # self.recipient_blood_type = recipient_blood_type
