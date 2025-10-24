-- ==========================================================
--  This SQL Script is for adding FOREIGN KEYS
-- ==========================================================

USE dbApp;

-- ==========================================================
--   EVENTS CORE AND SUBTABLES
-- ==========================================================

--
-- Constraints for `Event`
--
ALTER TABLE Events
ADD CONSTRAINT fk_event_artist
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_event_fanclub
    FOREIGN KEY (`Fanclub_ID`) REFERENCES Fanclub(`Fanclub_ID`)
    ON DELETE SET NULL ON UPDATE CASCADE,
ADD CONSTRAINT fk_event_venue
    FOREIGN KEY (`Venue_ID`) REFERENCES Venue(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT chk_event_host_xor
CHECK (
    (artist_id IS NOT NULL AND fanclub_id IS NULL)
 OR (artist_id IS NULL AND fanclub_id IS NOT NULL)
);

-- 
-- Constraints for `Section`
-- 
ALTER TABLE Section
ADD CONSTRAINT fk_section_venue
    FOREIGN KEY (`Venue_ID`) REFERENCES Venue(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Seats`
-- 
ALTER TABLE Seat
ADD CONSTRAINT fk_seat_venue
    FOREIGN KEY (`Venue_ID`) REFERENCES Venue(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Tier`
-- 
ALTER TABLE Ticket_Tier
ADD CONSTRAINT fk_tier_event
    FOREIGN KEY (`Event_ID`) REFERENCES `Event`(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Purchases`
-- 
ALTER TABLE Ticket_Purchase
ADD CONSTRAINT fk_tickets_user
    FOREIGN KEY (`User_ID`) REFERENCES User(`User_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_event
    FOREIGN KEY (`Event_ID`) REFERENCES `Events`(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_tier
    FOREIGN KEY (`Tier_ID`) REFERENCES Ticket_Tier(`Tier_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_seat
    FOREIGN KEY (`Seat_ID`) REFERENCES Seat(`Seats_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Artist`
-- 
ALTER TABLE Artist
ADD CONSTRAINT fk_artist_manager
    FOREIGN KEY (`Manager_ID`) REFERENCES Manager(`Manager_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Member_Detail`
-- 
ALTER TABLE Member_Detail
ADD CONSTRAINT fk_artist_member_detail
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Artist_Event`
-- 
ALTER TABLE Artist_Event
ADD CONSTRAINT fk_artist_event
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_event_artist
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Setlist`
-- 
ALTER TABLE Setlist
ADD CONSTRAINT fk_setlist_artist_event
	FOREIGN KEY (`Artist_ID`, `Event_ID`) REFERENCES Artist_Event(`Artist_ID`, `Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
