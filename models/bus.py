from .database import db

class Bus(db.Model):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "bus_number": self.bus_number, "capacity": self.capacity}
