from models.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        """
        Retourne une représenttation dictionnaire de la facture.
        """
        return {"id": self.id, "name": self.name, "email": self.email}
