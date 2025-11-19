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
-- Constraints for `Event`
--
ALTER TABLE LINK_Event_Type
ADD CONSTRAINT fk_link_type
    FOREIGN KEY (`Type_ID`) REFERENCES REF_Event_Type(`Type_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_link_event
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- 
-- Constraints for `Venue`
-- 
ALTER TABLE Venue
ADD CONSTRAINT fk_city_country
    FOREIGN KEY (`Location`) REFERENCES Location_Country(`Location`)
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

DROP PROCEDURE IF EXISTS generate_seats_for_section;
DELIMITER $$
DROP PROCEDURE IF EXISTS generate_seats_for_section;

DELIMITER $$

CREATE FUNCTION get_row_label(i INT)
RETURNS VARCHAR(10)
DETERMINISTIC
BEGIN
    DECLARE letters VARCHAR(26) DEFAULT 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    DECLARE label VARCHAR(10) DEFAULT '';
    DECLARE idx INT;

    WHILE i >= 0 DO
        SET idx = i % 26;
        SET label = CONCAT(SUBSTRING(letters, idx + 1, 1), label);
        SET i = FLOOR(i / 26) - 1;
    END WHILE;

    RETURN label;
END$$

CREATE PROCEDURE generate_seats_for_section(
    IN venue_id INT,
    IN section_id INT,
    IN section_capacity INT
)
BEGIN
    DECLARE seats_per_row INT DEFAULT 30;
    DECLARE row_index INT DEFAULT 0;
    DECLARE seat_num INT;
    DECLARE max_rows INT;

    SET max_rows = CEIL(section_capacity / seats_per_row);

    seat_loop: LOOP
        IF row_index >= max_rows THEN
            LEAVE seat_loop;
        END IF;

        SET seat_num = 1;

        seat_number_loop: LOOP
            IF (row_index * seats_per_row + seat_num) > section_capacity THEN
                LEAVE seat_number_loop;
            END IF;

            INSERT INTO Seat (Venue_ID, Section_ID, Seat_Row, Seat_Number)
            VALUES (
                venue_id,
                section_id,
                get_row_label(row_index),
                seat_num
            );

            SET seat_num = seat_num + 1;
            IF seat_num > seats_per_row THEN
                LEAVE seat_number_loop;
            END IF;
        END LOOP;

        SET row_index = row_index + 1;
    END LOOP seat_loop;

END$$

CREATE TRIGGER trg_generate_seats_after_section
AFTER INSERT ON Section
FOR EACH ROW
BEGIN
    CALL generate_seats_for_section(
        NEW.Venue_ID,
        NEW.Section_ID,
        NEW.Max_Capacity
    );
END$$

DELIMITER ;

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
-- Constraints for `Member`
-- 
ALTER TABLE Member
ADD CONSTRAINT fk_artist_member
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
    
DELIMITER $$

DROP TRIGGER IF EXISTS trg_member_status_check$$

CREATE TRIGGER trg_member_status_check
BEFORE INSERT ON Member
FOR EACH ROW
BEGIN
    DECLARE artist_status ENUM('Active', 'Inactive', 'Hiatus');

    SELECT Activity_Status
    INTO artist_status
    FROM Artist
    WHERE Artist_ID = NEW.Artist_ID;

    IF artist_status IN ('Hiatus', 'Inactive') THEN
        SET NEW.Activity_Status = artist_status;
    END IF;
END$$

DELIMITER ;
    
-- 
-- Constraints for `Member_Nationality`
-- 
ALTER TABLE LINK_Member_Nationality
ADD CONSTRAINT fk_member_member_nationality
    FOREIGN KEY (`Member_ID`) REFERENCES Member(`Member_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_nationality_member_nationality
    FOREIGN KEY (`Nationality_ID`) REFERENCES REF_Nationality(`Nationality_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
    
-- 
-- Constraints for `Member_Role`
-- 
ALTER TABLE LINK_Member_Role
ADD CONSTRAINT fk_member_member_role
    FOREIGN KEY (`Member_ID`) REFERENCES Member(`Member_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_nationality_member_role
    FOREIGN KEY (`Role_ID`) REFERENCES REF_Role(`Role_ID`)
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
ADD CONSTRAINT fk_setlist_artist
    FOREIGN KEY (`Artist_ID`) REFERENCES Artist(`Artist_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_setlist_event
    FOREIGN KEY (`Event_ID`) REFERENCES Event(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_setlist_artist_event
	FOREIGN KEY (`Artist_ID`, `Event_ID`) REFERENCES Artist_Event(`Artist_ID`, `Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_setlist_song
    FOREIGN KEY (`Song_ID`) REFERENCES Song(`Song_ID`)
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
	ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_merch_fanclub
    FOREIGN KEY (`Fanclub_ID`) REFERENCES `Fanclub`(`Fanclub_ID`)
	ON DELETE CASCADE ON UPDATE CASCADE,

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
    FOREIGN KEY (`Merchandise_ID`) REFERENCES `Merchandise`(`Merchandise_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for `Merchandise_Event`
--
ALTER TABLE `Merchandise_Event`
ADD CONSTRAINT fk_merchandiseevent_merch
    FOREIGN KEY (`Merchandise_ID`) REFERENCES `Merchandise`(`Merchandise_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_merchandiseevent_event
    FOREIGN KEY (`Event_ID`) REFERENCES `Event`(`Event_ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;
