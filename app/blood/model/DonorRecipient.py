from .. import db
class DonorRecipient(db.Model):
  __tablename__ = 'tbl_recipient_donor'
  id = db.Column(db.Integer, primary_key = True)
  recipient_id = db.Column(db.Integer)
  # lastname = db.Column(db.String(100))
  donor_id = db.Column(db.Integer)
  # posted_date = db.Column(db.DateTime)

  # recipeint_name = db.Column(db.String(100))
  # recipient_blood_type = db.Column(db.String(10))

  # password= db.Column(db.String(54))

  def __init__(self, recipient_id, donor_id):
    self.recipient_id = recipient_id
    self.donor_id = donor_id
    # self.posted_date = posted_date
