# model/models.py

from view.__init__ import db 
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.mysql import ENUM, SET

# ===============================================
#                 CORE TABLES
# ===============================================

class Fan(db.Model):
    Fan_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    First_Name = db.Column(db.String(255), nullable=False)
    Last_Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Date_Joined = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    Days_Since = db.Column(db.Integer, nullable=False)
    
    # Relationships
    orders = db.relationship('Order', backref='fan', lazy=True)
    ticket_purchases = db.relationship('TicketPurchase', backref='fan', lazy=True)
    memberships = db.relationship('FanclubMembership', backref='fan', lazy=True)
    artist_followers = db.relationship('ArtistFollower', backref='fan', lazy=True)

class Manager(db.Model):
    Manager_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Manager_Name = db.Column(db.String(255), nullable=False)
    Contact_Num = db.Column(db.String(11))
    Contact_Email = db.Column(db.String(255))
    Agency_Address = db.Column(db.String(255))
    
    # Relationships
    artists = db.relationship('Artist', backref='manager', lazy=True)

class Artist(db.Model):
    Artist_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key
    Manager_ID = db.Column(db.Integer, db.ForeignKey('manager.Manager_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Artist_Name = db.Column(db.String(255), nullable=False)
    Nationality = db.Column(db.String(255))
    Activity_Status = db.Column(ENUM('Active', 'Inactive', 'Hiatus'), nullable=False) 
    Debut_Date = db.Column(db.Date, nullable=False)
    Debut_Days = db.Column(db.Integer, nullable=False)
    
    # Relationships
    merchandise = db.relationship('Merchandise', backref='artist', lazy=True)
    fanclubs = db.relationship('Fanclub', backref='artist', lazy=True)
    member_details = db.relationship('MemberDetail', backref='artist', lazy=True)
    setlists = db.relationship('Setlist', backref='artist', lazy=True)
    events_association = db.relationship('ArtistEvent', backref='artist', lazy=True) # For Artist_Event Many-to-Many


class Venue(db.Model):
    Venue_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Venue_Name = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255), nullable=False)
    Capacity = db.Column(db.Integer, nullable=False)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Venue_Name', 'Country', 'City'),
        CheckConstraint('Capacity > 0')
    )
    
    # Relationships
    events = db.relationship('Event', backref='venue', lazy=True)
    sections = db.relationship('Section', backref='venue', lazy=True)
    seats = db.relationship('Seat', backref='venue', lazy=True)


class Event(db.Model):
    Event_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Name = db.Column(db.String(100), nullable=False)
    Event_Type = db.Column(SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve'), nullable=False) 
    # Foreign Key
    Venue_ID = db.Column(db.Integer, db.ForeignKey('venue.Venue_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Start_Date = db.Column(db.Date, nullable=False)
    End_Date = db.Column(db.Date, nullable=False)
    Start_Time = db.Column(db.Time, nullable=False)
    End_Time = db.Column(db.Time)

    # Constraints
    __table_args__ = (
        CheckConstraint('End_Date >= Start_Date', name='is_valid_date'),
    )
    
    # Relationships
    merchandise = db.relationship('Merchandise', backref='event', lazy=True)
    ticket_tiers = db.relationship('TicketTier', backref='event', lazy=True)
    ticket_purchases = db.relationship('TicketPurchase', backref='event', lazy=True)
    artist_association = db.relationship('ArtistEvent', backref='event', lazy=True) # For Artist_Event Many-to-Many
    fanclub_association = db.relationship('FanclubEvent', backref='event', lazy=True) # For Fanclub_Event Many-to-Many


class Merchandise(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    # Foreign Keys
    Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.Artist_ID', onupdate='CASCADE'), nullable=False)
    Event_ID = db.Column(db.Integer, db.ForeignKey('event.Event_ID', ondelete='CASCADE', onupdate='CASCADE'))
    Fanclub_ID = db.Column(db.Integer, db.ForeignKey('fanclub.Fanclub_ID', onupdate='CASCADE'))
    Description = db.Column(db.String(500))
    Price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    Initial_Stock = db.Column(db.Integer, nullable=False, default=0)
    Quantity_Stock = db.Column(db.Integer, nullable=False, default=0)

    # Constraints
    __table_args__ = (
        UniqueConstraint('Event_ID', 'Name'),
        CheckConstraint('Price >= 0'),
        CheckConstraint('Initial_Stock >= 0'),
        CheckConstraint('Quantity_Stock >= 0')
    )
    
    # Relationships
    purchase_lists = db.relationship('PurchaseList', backref='merchandise', lazy=True)


# ================================================
#              ADDITIONAL TABLES
# ================================================

class Fanclub(db.Model):
    Fanclub_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fanclub_Name = db.Column(db.String(255), nullable=False)
    # Foreign Key
    Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.Artist_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Fanclub_Name', 'Artist_ID'),
    )
    
    # Relationships
    merchandise = db.relationship('Merchandise', backref='fanclub', lazy=True)
    memberships = db.relationship('FanclubMembership', backref='fanclub', lazy=True)
    events_association = db.relationship('FanclubEvent', backref='fanclub', lazy=True) # For Fanclub_Event Many-to-Many


# --- Association Tables (Many-to-Many) ---

class ArtistEvent(db.Model):
    # Foreign Keys (Composite PK/FK)
    Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.Artist_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Event_ID = db.Column(db.Integer, db.ForeignKey('event.Event_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    
    # Relationship for Setlist (using composite FK/PK)
    setlists = db.relationship('Setlist', backref='artist_event_link', lazy=True, 
                               primaryjoin="and_(ArtistEvent.Artist_ID==Setlist.Artist_ID, ArtistEvent.Event_ID==Setlist.Event_ID)")


class FanclubEvent(db.Model):
    # Foreign Keys (Composite PK/FK)
    Fanclub_ID = db.Column(db.Integer, db.ForeignKey('fanclub.Fanclub_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Event_ID = db.Column(db.Integer, db.ForeignKey('event.Event_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


# --- Supporting Tables ---

class TicketTier(db.Model):
    Tier_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key
    Event_ID = db.Column(db.Integer, db.ForeignKey('event.Event_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Tier_Name = db.Column(db.String(100), nullable=False, default='General Admissions')
    Price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    Total_Quantity = db.Column(db.Integer, nullable=False, default=0)
    Benefits = db.Column(db.String(150))
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Event_ID', 'Tier_Name'),
    )
    
    # Relationships
    ticket_purchases = db.relationship('TicketPurchase', backref='tier', lazy=True)


class Section(db.Model):
    Section_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key
    Venue_ID = db.Column(db.Integer, db.ForeignKey('venue.Venue_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Section_Name = db.Column(db.String(255), nullable=False)
    Max_Capacity = db.Column(db.Integer, nullable=False)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Venue_ID', 'Section_Name'),
        CheckConstraint('Max_Capacity > 0')
    )
    
    # Relationships
    seats = db.relationship('Seat', backref='section', lazy=True)


class Seat(db.Model):
    Seat_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Keys
    Venue_ID = db.Column(db.Integer, db.ForeignKey('venue.Venue_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Section_ID = db.Column(db.Integer, db.ForeignKey('section.Section_ID'), nullable=False) # No CASCADE needed as Venue handles main deletion
    Seat_Row = db.Column(db.String(2), nullable=False)
    Seat_Number = db.Column(db.Integer, nullable=False)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Venue_ID', 'Section_ID', 'Seat_Row', 'Seat_Number'),
    )
    
    # Relationships
    ticket_purchases = db.relationship('TicketPurchase', backref='seat', lazy=True)


class MemberDetail(db.Model):
    Member_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key
    Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.Artist_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Member_Name = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(255))
    Activity_Status = db.Column(ENUM('Active', 'Inactive', 'Hiatus'), nullable=False)
    Birth_Date = db.Column(db.Date)
    Age = db.Column(db.Integer)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Artist_ID', 'Member_ID', name='uk_artist_member_id'),
    )


class Setlist(db.Model):
    # Foreign Keys (Part of Composite PK)
    Artist_ID = db.Column(db.Integer, primary_key=True)
    Event_ID = db.Column(db.Integer, primary_key=True)
    
    # Composite Foreign Key referencing ArtistEvent
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['Artist_ID', 'Event_ID'],
            ['artist_event.Artist_ID', 'artist_event.Event_ID'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        # You need the columns declared as PKs first
        db.Column('Song_Name', db.String(255), nullable=False),
        db.Column('Play_Order', db.Integer, nullable=False, primary_key=True)
    )


# ==============================================
#             TRANSACTION TABLES
# ==============================================

class Order(db.Model):
    Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key
    Fan_ID = db.Column(db.Integer, db.ForeignKey('fan.Fan_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Order_Date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    Status = db.Column(ENUM('Pending', 'Paid', 'Cancelled', 'Refunded'), nullable=False, default='Pending')
    
    # Relationships
    purchase_lists = db.relationship('PurchaseList', backref='order', lazy=True)


class PurchaseList(db.Model):
    Purchase_List_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Keys
    Order_ID = db.Column(db.Integer, db.ForeignKey('order.Order_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Merchandise_ID = db.Column(db.Integer, db.ForeignKey('merchandise.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('Quantity > 0'),
    )


class TicketPurchase(db.Model):
    Ticket_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Keys
    Fan_ID = db.Column(db.Integer, db.ForeignKey('fan.Fan_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Event_ID = db.Column(db.Integer, db.ForeignKey('event.Event_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Tier_ID = db.Column(db.Integer, db.ForeignKey('ticket_tier.Tier_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Seat_ID = db.Column(db.Integer, db.ForeignKey('seat.Seat_ID', ondelete='CASCADE', onupdate='CASCADE'))
    Purchase_Date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Event_ID', 'Tier_ID', 'Seat_ID', name='is_ticket_unique'),
    )


class FanclubMembership(db.Model):
    Membership_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Keys
    Fan_ID = db.Column(db.Integer, db.ForeignKey('fan.Fan_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Fanclub_ID = db.Column(db.Integer, db.ForeignKey('fanclub.Fanclub_ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Date_Joined = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('Fan_ID', 'Fanclub_ID'),
    )


class ArtistFollower(db.Model):
    # Foreign Keys
    Artist_ID = db.Column(db.Integer, db.ForeignKey('artist.Artist_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Fan_ID = db.Column(db.Integer, db.ForeignKey('fan.Fan_ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)