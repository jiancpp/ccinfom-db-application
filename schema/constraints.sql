-- ==========================================================
--  This SQL Script is for adding FOREIGN KEYS
-- ==========================================================

USE dbApp;

-- ==========================================================
--   EVENTS CORE AND SUBTABLES
-- ==========================================================

--
-- Constraints for `Events`
--
ALTER TABLE Events
ADD CONSTRAINT fk_events_artists
    FOREIGN KEY (`Artist_ID`) REFERENCES Artists(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_events_fanclubss
    FOREIGN KEY (`Fanclub_ID`) REFERENCES Fanclubs(`Fanclub_ID`)
    ON DELETE SET NULL ON UPDATE CASCADE,
ADD CONSTRAINT fk_events_venue
    FOREIGN KEY (`Venue_ID`) REFERENCES Venues(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT chk_event_host_xor
CHECK (
    (artist_id IS NOT NULL AND fanclub_id IS NULL)
 OR (artist_id IS NULL AND fanclub_id IS NOT NULL)
);

-- 
-- Constraints for `Sections`
-- 
ALTER TABLE Sections
ADD CONSTRAINT fk_sections_venues
    FOREIGN KEY (`Venue_ID`) REFERENCES Venues(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Seats`
-- 
ALTER TABLE Seats
ADD CONSTRAINT fk_seats_venues
    FOREIGN KEY (`Venue_ID`) REFERENCES Venues(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Tier`
-- 
ALTER TABLE Ticket_Tiers
ADD CONSTRAINT fk_tiers_events
    FOREIGN KEY (`Event_ID`) REFERENCES Events(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Purchases`
-- 
ALTER TABLE Ticket_Purchases
ADD CONSTRAINT fk_tickets_users
    FOREIGN KEY (`User_ID`) REFERENCES Users(`User_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_tickets_events
    FOREIGN KEY (`Event_ID`) REFERENCES Events(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_tickets_tiers
    FOREIGN KEY (`Tier_ID`) REFERENCES Ticket_Tiers(`Tier_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_tickets_seats
    FOREIGN KEY (`Seat_ID`) REFERENCES Seats(`Seats_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
