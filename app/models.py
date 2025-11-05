from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import SET
from sqlalchemy import DECIMAL, text

db = SQLAlchemy()

# ============================================
#  Tables assigned to: @jiancpp
# ============================================

class Event(db.Model):
    __tablename__ = "Event"

    Event_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Name = db.Column(db.String(100), nullable=False)
    # SQL SET maps to SQLAlchemy Enum
    Event_Type = db.Column(SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve'), nullable=False)
    Venue_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Venue.Venue_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False)
    Start_Date = db.Column(db.Date, nullable=False)
    End_Date = db.Column(db.Date, nullable=False)
    Start_Time = db.Column(db.Time, nullable=False)
    End_Time = db.Column(db.Time)

    # Relationships
    venue = db.relationship("Venue", back_populates="events")
    ticket_tiers = db.relationship("Ticket_Tier", back_populates="event", cascade="all, delete-orphan")
    ticket_purchases = db.relationship("Ticket_Purchase", back_populates="event", cascade="all, delete-orphan")
    # artist_events
    # fanclub_events
    # merchandises

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
    Capacity = db.Column(db.Integer, nullable=False)

    # Relationships (FK and tables where Venue is referenced)
    events = db.relationship("Event", back_populates="venue")
    sections = db.relationship("Section", back_populates="venue", cascade="all, delete-orphan")
    seats = db.relationship("Seat", back_populates="venue", cascade="all, delete-orphan")

    # Constraint 
    __table_args__ = (
        db.UniqueConstraint("Venue_Name", "Country", "City"),
        db.CheckConstraint("Capacity > 0"),
    )


class Section(db.Model):
    __tablename__ = "Section"

    Section_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Venue_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Venue.Venue_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False)
    Section_Name = db.Column(db.String(255), nullable=False)
    Max_Capacity = db.Column(db.Integer, nullable=False)

    # Relationships
    venue = db.relationship("Venue", back_populates="sections")
    seats = db.relationship("Seat", back_populates="section", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Venue_ID", "Section_Name"),
        db.CheckConstraint("Max_Capacity > 0"),
    )

class Seat(db.Model):
    __tablename__ = "Seat"

    Seat_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Venue_ID = db.Column(
        db.Integer,
        db.ForeignKey("Venue.Venue_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False)
    Section_ID = db.Column(
        db.Integer,
        db.ForeignKey("Section.Section_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    Seat_Row = db.Column(db.String(2), nullable=False)
    Seat_Number = db.Column(db.Integer, nullable=False)

    # Relationship
    venue = db.relationship("Venue", back_populates="seats")
    section = db.relationship("Section", back_populates="seats")
    ticket_purchases = db.relationship("Ticket_Purchase", back_populates="seat")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Venue_ID", "Section_ID", "Seat_Row", "Seat_Number"),
    )
    
class Ticket_Tier(db.Model):
    __tablename__ = "Ticket_Tier"

    Tier_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_ID = db.Column(
        db.Integer,
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False)
    Tier_Name = db.Column(db.String(100), nullable=False, server_default=text("General Admissions"))
    Price = db.Column(DECIMAL(10,2), nullable=False, server_default=text("0.00"))
    Total_Quantity = db.Column(db.Integer, nullable=False, server_default=text("0"))
    Benefits = db.Column(db.String(150))

    # Relationships
    event = db.relationship("Event", back_populates="ticket_tiers")
    ticket_purchases = db.relationship("Ticket_Purchase", back_populates="ticket_tier", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Event_ID", "Tier_Name"),
        db.CheckConstraint("Price >= 0", name="tier_price_nonnegative"),
    )

class Ticket_Purchase(db.Model):
    __tablename__ = "Ticket_Purchase"

    Ticket_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Fan_ID = db.Column(db.Integer, db.ForeignKey(...))
    Event_ID = db.Column(
        db.Integer,
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    Tier_ID = db.Column(
        db.Integer,
        db.ForeignKey("Ticket_Tier.Tier_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    Seat_ID = db.Column(
        db.Integer,
        db.ForeignKey("Seat.Seat_ID", ondelete="CASCADE", onupdate="CASCADE")
    )
    Purchase_Date = db.Column(db.DateTime, nullable=False, default=func.now())

    # Relationships
    # fan
    event = db.relationship("Event", back_populates="ticket_purchases")
    ticket_tier = db.relationship("Ticket_Tier", back_populates="ticket_purchases")
    seat = db.relationship("Seat", back_populates="ticket_purchases")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Event_ID", "Tier_ID", "Seat_ID", name="is_ticket_unique"),
    )

# ============================================
#  Tables assigned to: @eepy
# ============================================
    

# ============================================
#  Tables assigned to: @jesmaeca
# ============================================
    

# ============================================
#  Tables assigned to: @phlmn
# ============================================