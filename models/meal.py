from database import db

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(80), nullable=False) 
  date = db.Column(db.DateTime(), nullable=False)
  fit = db.Column(db.Boolean, nullable=False, default=True)
  
  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "date": self.date,
      "fit": self.fit,
    }
  