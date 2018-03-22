from .. import db
class BloodCategory(db.Model):
	__tablename__ ='tbl_bloodcategory'
	id = db.Column(db.Integer,primary_key=True)
	blood_type = db.Column(db.String(100))

	def __init__(self, blood_type):
		self.blood_type = blood_type.title()
