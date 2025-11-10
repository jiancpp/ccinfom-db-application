from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import SET, TINYINT
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
    artists = db.relationship("Artist", secondary="Artist_Event", back_populates="events")
    fanclubs = db.relationship("Fanclub", secondary="Fanclub_Event", back_populates="events")
    merchandise = db.relationship("Merchandise", back_populates="event", cascade="all, delete-orphan")
    setlists = db.relationship("Setlist", back_populates="event")
    
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
        db.UniqueConstraint("Venue_Name", "Country", "City", name="is_venue_unique"),
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
    ticket_tiers = db.relationship("Ticket_Tier", secondary="Tier_Section", back_populates="sections")

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
    Seat_Row = db.Column(db.String(5), nullable=False)
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
    Is_Reserved_Seating = db.Column(TINYINT, server_default=text("0"))
    


    # Relationships
    event = db.relationship("Event", back_populates="ticket_tiers")
    ticket_purchases = db.relationship("Ticket_Purchase", back_populates="ticket_tier", cascade="all, delete-orphan")
    sections = db.relationship("Section", secondary="Tier_Section", back_populates="ticket_tiers")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Event_ID", "Tier_Name"),
        db.CheckConstraint("Price >= 0", name="tier_price_nonnegative"),
    )

class TierSection(db.Model):
    __tablename__ = "Tier_Section"

    Tier_ID = db.Column(db.Integer, db.ForeignKey("Ticket_Tier.Tier_ID"), primary_key=True)
    Section_ID = db.Column(db.Integer, db.ForeignKey("Section.Section_ID"), primary_key=True)


class Ticket_Purchase(db.Model):
    __tablename__ = "Ticket_Purchase"

    Ticket_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fan_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Fan.Fan_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False
    )
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
    fan = db.relationship("Fan", back_populates="ticket_purchases")
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
class Fan(db.Model):
    __tablename__ = "Fan"

    Fan_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    First_Name = db.Column(db.String(255), nullable=False)
    Last_Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Date_Joined = db.Column(db.DateTime, nullable=False, default=func.now())
    Days_Since = db.Column(db.Integer, nullable=False) 

    # Relationships
    memberships = db.relationship("Fanclub_Membership", back_populates="fan", cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="fan")
    ticket_purchases = db.relationship("Ticket_Purchase", back_populates="fan")
    artists_following = db.relationship("Artist", secondary="Artist_Follower", back_populates="followers")

class Fanclub(db.Model):
    __tablename__ = "Fanclub"

    Fanclub_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fanclub_Name = db.Column(db.String(255), nullable=False)
    Artist_ID = db.Column(db.Integer, nullable=False) 
    
    # Relationships
    members = db.relationship("Fanclub_Membership", back_populates="fanclub", cascade="all, delete-orphan")
    events = db.relationship("Event", secondary="Fanclub_Event", back_populates="fanclubs")
    merchandise = db.relationship("Merchandise", back_populates="fanclub", lazy='dynamic')

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Fanclub_Name", "Artist_ID"),
    )

class Fanclub_Membership(db.Model):
    __tablename__ = "Fanclub_Membership"

    Membership_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    Fan_ID = db.Column(
        db.Integer,
        db.ForeignKey("Fan.Fan_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    Fanclub_ID = db.Column(
        db.Integer,
        db.ForeignKey("Fanclub.Fanclub_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    Date_Joined = db.Column(db.DateTime, nullable=False, default=func.now())

    # Relationships
    fan = db.relationship("Fan", back_populates="memberships")
    fanclub = db.relationship("Fanclub", back_populates="members")

    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Fan_ID", "Fanclub_ID"),
    )

class Fanclub_Event(db.Model):
    __tablename__ = "Fanclub_Event"
    
    Fanclub_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Fanclub.Fanclub_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )
    Event_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )



# ============================================
#  Tables assigned to: @jesmaeca
# ============================================

class Artist(db.Model):
    __tablename__ = "Artist"

    Artist_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Manager_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Manager.Manager_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False)
    Artist_Name = db.Column(db.String(100), nullable=False)
    # SQL SET maps to SQLAlchemy Enum
    Activity_Status = db.Column(SET('Active', 'Inactive', 'Hiatus'), nullable=False)
    Debut_Date = db.Column(db.Date, nullable=False)
    Debut_Days= db.Column(db.Integer, nullable=False)

    # Relationships
    manager = db.relationship("Manager", back_populates="artist")
    member_detail = db.relationship("Member_Detail", back_populates="artist")
    followers = db.relationship("Fan", secondary="Artist_Follower", back_populates="artists_following")
    events = db.relationship("Event", secondary="Artist_Event", back_populates="artists")
    merchandise = db.relationship("Merchandise", back_populates="artist")
    setlists = db.relationship("Setlist", back_populates="artist")

class Member_Detail(db.Model):
    __tablename__ = "Member_Detail"

    Member_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Artist_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Artist.Artist_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False
    )
    Member_Name = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(100), nullable=True)
    Nationality = db.Column(db.String(100), nullable=True)
    # SQL SET maps to SQLAlchemy Enum
    Activity_Status = db.Column(SET('Active', 'Inactive', 'Hiatus'), nullable=False)
    Birth_Date = db.Column(db.Date, nullable=False)
    Age = db.Column(db.Integer, nullable=False)

    # Relationships
    artist = db.relationship("Artist", back_populates="member_detail")

class Manager(db.Model):
    __tablename__ = "Manager"

    Manager_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Manager_Name = db.Column(db.String(100), nullable=False)
    Contact_Num = db.Column(db.String(20), nullable=True)
    Contact_Email = db.Column(db.String(100), nullable=True)
    Agency_Address = db.Column(db.String(100), nullable=True)

    artist = db.relationship("Artist", back_populates="manager")

class Setlist(db.Model):
    __tablename__ = "Setlist"

    Artist_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Artist.Artist_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )
    Event_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    Song_Name = db.Column(db.String(100), nullable=True)
    Play_Order = db.Column(db.Integer, nullable = False)

    artist = db.relationship("Artist", back_populates="setlists")
    event = db.relationship("Event", back_populates="setlists")

class Artist_Follower(db.Model):
    __tablename__ = "Artist_Follower"

    Artist_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Artist.Artist_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )
    Fan_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Fan.Fan_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )

class Artist_Event(db.Model):
    __tablename__ = "Artist_Event"

    Artist_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Artist.Artist_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )
    Event_ID = db.Column(
        db.Integer, 
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )

# ============================================
#  Tables assigned to: @phlmn
# ============================================
# merchandise
class Merchandise(db.Model):
    __tablename__ = "Merchandise"
    Merchandise_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Merchandise_Name = db.Column(db.String(100), nullable=False)
    
    Artist_ID = db.Column(
        db.Integer,
        db.ForeignKey("Artist.Artist_ID", ondelete="CASCADE", onupdate="CASCADE"))
    Event_ID = db.Column(
        db.Integer,
        db.ForeignKey("Event.Event_ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False)
    Fanclub_ID = db.Column(
        db.Integer,
        db.ForeignKey("Fanclub.Fanclub_ID", ondelete="CASCADE", onupdate="CASCADE"))
    
    Merchandise_Description = db.Column(db.String(500), nullable=False)
    Merchandise_Price = db.Column(DECIMAL(10,2), nullable=False, server_default=text("0.00"))
    Initial_Stock = db.Column(db.Integer, nullable=False, server_default=text("0"))
    Quantity_Stock = db.Column(db.Integer, nullable=False, server_default=text("0"))
    
    # Relationships
    artist = db.relationship("Artist", back_populates="merchandise")
    event = db.relationship("Event", back_populates="merchandise")
    fanclub = db.relationship("Fanclub", back_populates="merchandise")
    purchase_list = db.relationship("Purchase_List", back_populates="merchandise", cascade="all, delete")
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Merchandise_ID", "Merchandise_Name"),
        db.CheckConstraint("Merchandise_Price > 0.00", "Initial_Stock > 0", "Quantity_Stock > 0"),
    )
    
#order
class Order(db.Model):
    __tablename__ = "Order"
    Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    Fan_ID = db.Column(
        db.Integer,
        db.ForeignKey("Fan.Fan_ID", ondelete="CASCADE", onupdate="CASCADE"))
    
    Order_Date = db.Column(db.DateTime, nullable=False, default=func.now())
    Order_Status = db.Column(SET('Pending', 'Paid', 'Cancelled'), nullable=False, default='Pending')
    
    # Relationships
    fan = db.relationship("Fan", back_populates="orders")
    purchase_list = db.relationship("Purchase_List", back_populates="order", cascade="all, delete")
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Order_ID"),
    )

    
#purchase list
class Purchase_List(db.Model):
    __tablename__ = "Purchase_List"
    Purchase_List_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Order_ID = db.Column(
        db.Integer,
        db.ForeignKey("Order.Order_ID", ondelete="CASCADE", onupdate="CASCADE"))
    
    Merchandise_ID = db.Column(
        db.Integer,
        db.ForeignKey("Merchandise.Merchandise_ID", ondelete="CASCADE", onupdate="CASCADE"))
    
    Quantity_Purchased = db.Column(db.Integer, nullable=False, default=1)
    
    # Relationships
    order = db.relationship("Order", back_populates="purchase_list")
    merchandise = db.relationship("Merchandise", back_populates="purchase_list")
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint("Purchase_List_ID"),
        db.CheckConstraint("Quantity_Purchased > 0.00"),
    )
