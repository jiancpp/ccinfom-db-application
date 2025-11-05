from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import SET

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = "Event"

    Event_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Name = db.Column(db.String(100), nullable=False)
    # SQL SET maps to SQLAlchemy Enum
    Event_Type = db.Column(SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve'), nullable=False)
    Venue_ID = db.Column(db.Integer, db.ForeignKey("Venue.Venue_ID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Start_Date = db.Column(db.Date, nullable=False)
    End_Date = db.Column(db.Date, nullable=False)
    Start_Time = db.Column(db.Time, nullable=False)
    End_Time = db.Column(db.Time)

    # Relationship with Venue
    venue = db.relationship("Venue", back_populates="events")
    # ticket_tier
    # ticket

    # Constraints
    __table_args__ = (
        db.CheckConstraint(
            "(End_Date > Start_Date) OR (End_Date = Start_Date AND End_Time > Start_Time)",
            name="is_valid_datetime"
        ),
    )


class Venue(db.Model):
    __tablename__ = "Venue"

    Venue_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Venue_Name = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255), nullable=False)
    Capacity = db.Column(db.Integer, db.CheckConstraint("Capacity > 0"), nullable=False)

    # Relationships (child tables reference Venue_ID as FK)
    events = db.relationship("Event", back_populates="venue")
    # sections = db.relationship("Section", back_populates="venue")
    # seats = db.relationship("Seat", back_populates="venue")

    # Unique constraint on name + country + city
    __table_args__ = (db.UniqueConstraint("Venue_Name", "Country", "City"),)
