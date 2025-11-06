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
ALTER TABLE Event
ADD CONSTRAINT fk_event_venue
    FOREIGN KEY (`Venue_ID`) REFERENCES Venue(`Venue_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

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

ALTER TABLE Tier_Section
ADD CONSTRAINT fk_tier
	FOREIGN KEY (`Tier_ID`) REFERENCES Ticket_Tier(`Tier_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_section
	FOREIGN KEY (`Section_ID`) REFERENCES Section(`Section_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Tier`
-- 
ALTER TABLE Ticket_Tier
ADD CONSTRAINT fk_tier_event
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Ticket_Purchases`
-- 
ALTER TABLE Ticket_Purchase
ADD CONSTRAINT fk_tickets_fan
    FOREIGN KEY (`Fan_ID`) REFERENCES Fan(`Fan_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_event
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_tier
    FOREIGN KEY (`Tier_ID`) REFERENCES Ticket_Tier(`Tier_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_ticket_seat
    FOREIGN KEY (`Seat_ID`) REFERENCES Seat(`Seat_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;


-- ==========================================================
--   ARTIST CORE AND SUBTABLES
-- ==========================================================

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


-- ==========================================================
--   FAN SUBTABLES
-- ==========================================================

-- 
-- Constraints for `Fanclub`
-- 
ALTER TABLE Fanclub
ADD CONSTRAINT fk_fanclub_artist
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- Constraints for `Fanclub_Event`
-- 
ALTER TABLE Fanclub_Event
ADD CONSTRAINT fk_fanevent_fanclub
    FOREIGN KEY (`Fanclub_ID`) REFERENCES Fanclub(`Fanclub_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_fanevent_event
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Fanclub_Membership`
-- 
ALTER TABLE Fanclub_Membership
ADD CONSTRAINT fk_membership_fan
    FOREIGN KEY (`Fan_ID`) REFERENCES Fan(`Fan_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_membership_fanclub
    FOREIGN KEY (`Fanclub_ID`) REFERENCES Fanclub(`Fanclub_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Artist_Follower`
-- 
ALTER TABLE Artist_Follower
ADD CONSTRAINT fk_artist_follower
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_follower_artist
    FOREIGN KEY (`Fan_ID`) REFERENCES Fan(`Fan_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;


-- ==========================================================
--   MERCHANDISE SUBTABLES
-- ==========================================================
-- 
-- Constraints for `Merchandise`
-- 
ALTER TABLE `Merchandise`
ADD CONSTRAINT fk_merch_artist
    FOREIGN KEY (`Artist_ID`) REFERENCES `Artist`(`Artist_ID`)
    ON UPDATE CASCADE,
ADD CONSTRAINT fk_merch_event
    FOREIGN KEY (`Event_ID`) REFERENCES `Event`(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_merch_fanclub
    FOREIGN KEY (`Fanclub_ID`) REFERENCES `Fanclub`(`Fanclub_ID`)
    ON UPDATE CASCADE;

-- 
-- Constraints for `Order`
-- 
ALTER TABLE `Order`
ADD CONSTRAINT fk_order_user
    FOREIGN KEY (`Fan_ID`) REFERENCES `Fan`(`Fan_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Purchase_List`
-- 
ALTER TABLE `Purchase_List`
ADD CONSTRAINT fk_purchaselist_order
    FOREIGN KEY (`Order_ID`) REFERENCES `Order`(`Order_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_purchaselist_merch
    FOREIGN KEY (`Merchandise_ID`) REFERENCES `Merchandise`(`ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
