-- ==========================================================
--  This SQL Script is ONLY FOR CREATING TABLES.
--  Add foreign keys on 'constraints.sql'
-- ==========================================================

DROP DATABASE IF EXISTS dbApp;
CREATE DATABASE dbApp;
USE dbApp;

-- ===============================================
--                  CORE TABLES
-- ===============================================

--
-- Table structure for table `Fan`
--
DROP TABLE IF EXISTS `Fan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fan` (
    `Fan_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Username` VARCHAR(255) NOT NULL,
    `First_Name` VARCHAR(255) NOT NULL,
    `Last_Name` VARCHAR(255) NOT NULL,
    `Email` VARCHAR(255) NOT NULL,
    `Date_Joined` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`Fan_ID`),
    UNIQUE (`Username`),
    UNIQUE (`Email`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Artist`
--
DROP TABLE IF EXISTS `Artist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist` (
	`Artist_ID` INT(11) NOT NULL AUTO_INCREMENT,
	`Manager_ID` INT(11),
    `Artist_Name` VARCHAR(255) NOT NULL,
	`Activity_Status` ENUM('Active', 'Inactive', 'Hiatus') NOT NULL,
    `Debut_Date` DATE NOT NULL,
    PRIMARY KEY (`Artist_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- 
-- Table structure for `Merchandise`
--
DROP TABLE IF EXISTS `Merchandise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Merchandise` (
	`Merchandise_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Merchandise_Name` VARCHAR(255) NOT NULL, -- Increased length
    `Artist_ID` INT(11),
    `Fanclub_ID` INT,
    `Merchandise_Description` VARCHAR(1000) DEFAULT NULL, -- Increased length
    `Merchandise_Price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `Initial_Stock` INT(6) NOT NULL DEFAULT 0,
    `Quantity_Stock` INT(6) NOT NULL DEFAULT 0,

    PRIMARY KEY (`Merchandise_ID`),
    UNIQUE (`Merchandise_Name`),
    
    CHECK (`Quantity_Stock` <= `Initial_Stock`),

	CHECK (`Merchandise_Price` >= 0),
    CHECK (`Initial_Stock` >= 1),
    CHECK (`Quantity_Stock` >= 1)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `Event`
--
DROP TABLE IF EXISTS `Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Event` (
    `Event_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Event_Name` VARCHAR(100) NOT NULL,
    `Venue_ID` INT(11) NOT NULL,
	`Start_Date` DATE NOT NULL,
	`End_Date` DATE NOT NULL,
	`Start_Time` TIME NOT NULL,
	`End_Time` TIME,

    PRIMARY KEY (`Event_ID`),
	CONSTRAINT is_valid_date CHECK(`Start_Date` <= `End_Date`),
    CONSTRAINT uk_event_name UNIQUE(`Event_Name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


-- ================================================
--               ADDITIONAL TABLES
-- ================================================

--
-- Table structure for `Fanclub`
--
DROP TABLE IF EXISTS `Fanclub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fanclub` (
    `Fanclub_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Fanclub_Name` VARCHAR(255) NOT NULL,
    `Artist_ID` INT(11) NOT NULL,
    
    PRIMARY KEY (`Fanclub_ID`),
    UNIQUE (`Fanclub_Name`)     -- Ensures that no two fanclubs of the same artist share a name
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Artist_Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Event` (
	`Artist_ID` INT(11) NOT NULL,
	`Event_ID` INT(11) NOT NULL,
    PRIMARY KEY (`Artist_ID`, `Event_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `Fanclub_Event`
--
DROP TABLE IF EXISTS `Fanclub_Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fanclub_Event` (
    `Fanclub_ID` INT(11) NOT NULL,
    `Event_ID` INT(11) NOT NULL,
    
    PRIMARY KEY (`Fanclub_ID`, `Event_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `Ticket_Tier`
--
DROP TABLE IF EXISTS `Ticket_Tier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ticket_Tier` (
    `Tier_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Event_ID` INT(11) NOT NULL,
    `Tier_Name` VARCHAR(100) DEFAULT 'General Admissions',
    `Price` DECIMAL(10,2) DEFAULT 0.00,
    `Total_Quantity` INT,
	`Benefits` VARCHAR(150),
    `Is_Reserved_Seating` TINYINT DEFAULT 0,
	
	PRIMARY KEY (`Tier_ID`),
    UNIQUE (`Event_ID`, `Tier_Name`)

    -- -- Ensures that there is enough slots available
    -- CONSTRAINT check_qty CHECK (`quantity_sold` <= `total_quantity`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `Venue`
--
DROP TABLE IF EXISTS `Venue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Venue` (
	`Venue_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Venue_Name` VARCHAR(255) NOT NULL, 
    `Location` VARCHAR(255),
    `Capacity` INT,
	`Is_Seated` TINYINT NOT NULL,
    
    PRIMARY KEY (`Venue_ID`),
    UNIQUE (`Venue_Name`, `Location`) -- Prevents duplicate venues with the same name and location
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- 
-- Table structure for table 'Section'
--
DROP TABLE IF EXISTS `Section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Section` (
	`Section_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Venue_ID` INT(11) NOT NULL, 
    `Section_Name` VARCHAR(255) NOT NULL, 
    `Max_Capacity` INT NOT NULL CHECK (Max_Capacity > 0),
    
    PRIMARY KEY (`Section_ID`),
    UNIQUE (Venue_ID, Section_Name) -- Prevents duplicate venues with the same name and location
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Seat`
--
DROP TABLE IF EXISTS `Seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seat` (
	`Seat_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Venue_ID` INT(11) NOT NULL,
    `Section_ID` INT(11) NOT NULL,
    `Seat_Row` VARCHAR(5) NOT NULL, 
    `Seat_Number` INT NOT NULL,
    
    PRIMARY KEY (`Seat_ID`),
	UNIQUE (`Venue_ID`, `Section_ID`, `Seat_Row`, `Seat_Number`) -- Prevents duplicates of the seat
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tier_Section`
--
DROP TABLE IF EXISTS `Tier_Section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE Tier_Section (
    Tier_ID INT,
    Section_ID INT,
    PRIMARY KEY (Tier_ID, Section_ID)
);

DROP TABLE IF EXISTS `Manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manager` (
	`Manager_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Manager_Name` VARCHAR(255) NOT NULL,
	`Contact_Num` VARCHAR(11),
    `Contact_Email` VARCHAR(255),
    `Agency` VARCHAR(255),
    PRIMARY KEY (`Manager_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Member` (
	`Member_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Artist_ID` INT(11) NOT NULL,
    `Member_Name` VARCHAR(255) NOT NULL,
    `Activity_Status` ENUM('Active', 'Inactive', 'Hiatus') NOT NULL,
    `Birth_Date` DATE, 
    PRIMARY KEY (`Member_ID`),
    UNIQUE KEY `uk_artist_member_id` (`Artist_ID`, `Member_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Setlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Setlist` (
	`Artist_ID` INT(11) NOT NULL,
	`Event_ID` INT(11) NOT NULL,
    `Song_Name` VARCHAR(255) NOT NULL,
    `Play_Order` INT(11) NOT NULL,
    PRIMARY KEY (`Artist_ID`, `Event_ID`, `Play_Order`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Setlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Setlist` (
	`Artist_ID` INT(11) NOT NULL,
	`Event_ID` INT(11) NOT NULL,
    `Song_ID` INT(11) NOT NULL,
    `Play_Order` INT(11) NOT NULL,
    PRIMARY KEY (`Artist_ID`, `Event_ID`, `Play_Order`),
    UNIQUE (`Artist_ID`, `Event_ID`, `Song_ID`),
    CHECK (`Play_Order` > 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Song` (
	`Song_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Song_Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`Song_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- ==============================================
--              TRANSACTION TABLES
-- ==============================================

-- 
-- Table structure for `order`
--
DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order` (
    `Order_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Fan_ID` INT(11) NOT NULL,
    `Order_Date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Order_Status` ENUM('Pending', 'Paid', 'Cancelled') NOT NULL DEFAULT 'Pending',

    PRIMARY KEY (`Order_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- 
-- Table structure for `Purchase List`
--
DROP TABLE IF EXISTS `Purchase_List`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Purchase_List` (
    `Purchase_List_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Order_ID` INT(11) NOT NULL,
    `Merchandise_ID` INT(11) NOT NULL,
    `Quantity_Purchased` INT(5) NOT NULL DEFAULT 1,

    PRIMARY KEY (`Purchase_List_ID`),
	CHECK (`Quantity_Purchased` > 0)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `Ticket_Purchase`
--
DROP TABLE IF EXISTS `Ticket_Purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ticket_Purchase` (
    `Ticket_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Fan_ID` INT(11) NOT NULL,
    `Event_ID` INT(11) NOT NULL,
    `Tier_ID` INT(11) NOT NULL,
    `Seat_ID` INT(11),
    `Purchase_Date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`Ticket_ID`),
    -- Ensures that only one seat per event and tier is sold
    -- (works for free seating where seat is NULL)
    CONSTRAINT is_ticket_unique UNIQUE (`Event_ID`, `Tier_ID`, `Seat_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Fanclub_Membership`
--
DROP TABLE IF EXISTS `Fanclub_Membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fanclub_Membership` (
    `Fan_ID` INT(11) NOT NULL,
    `Fanclub_ID` INT(11) NOT NULL,
    `Date_Joined` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`Fan_ID`, `Fanclub_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Artist_Follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Follower` (
	`Artist_ID` INT(11) NOT NULL,
    `Fan_ID` INT(11) NOT NULL, 
    `Followed_Date` DATE NOT NULL,
    
    PRIMARY KEY (`Artist_ID`, `Fan_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- ==============================================
--              REFERENCE TABLES
-- ==============================================

--
-- Table structure for table `Fanclub_Membership`
--
DROP TABLE IF EXISTS `REF_Event_Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `REF_Event_Type` (
    `Type_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Type_Name` VARCHAR(255) NOT NULL,
    `Artist_Event_Only` TINYINT DEFAULT 0,
    
    PRIMARY KEY (`Type_ID`),
    CONSTRAINT is_type_unique UNIQUE (`Type_Name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS `LINK_Event_Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `LINK_Event_Type` (
    `Event_ID` INT(11) NOT NULL,
    `Type_ID` INT(11) NOT NULL,
    
    PRIMARY KEY (`Event_ID`, `Type_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS `REF_Nationality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `REF_Nationality` (
	`Nationality_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Nationality_Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`Nationality_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `LINK_Member_Nationality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `LINK_Member_Nationality` (
	`Member_ID` INT(11) NOT NULL,
    `Nationality_ID` INT(11) NOT NULL,
    PRIMARY KEY (`Member_ID`, `Nationality_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `REF_Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `REF_Role` (
	`Role_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Role_Name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`Role_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `LINK_Member_Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `LINK_Member_Role` (
	`Member_ID` INT(11) NOT NULL,
    `Role_ID` INT(11) NOT NULL,
    PRIMARY KEY (`Member_ID`, `Role_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Location_Country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Location_Country` (
    `Location` VARCHAR(255) NOT NULL,
    `Country` VARCHAR(255) NOT NULL,
    
    PRIMARY KEY (`Location`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;


DROP TABLE IF EXISTS `Merchandise_Event`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Merchandise_Event` (
    `Merchandise_ID` INT(11) NOT NULL,
    `Event_ID` INT(11) NOT NULL,

    -- Define the composite primary key
    PRIMARY KEY (`Merchandise_ID`, `Event_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

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
	ON DELETE CASCADE ON UPDATE CASCADE;

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

INSERT INTO Fan (Username, First_Name, Last_Name, Email, Date_Joined) 
VALUES	('eloelo', 'Shielo', 'Lunario', 'shielo@gmail.com', '2021-01-01'),
		('jesmaeca', 'Jessica', 'Dela Cruz', 'jess@gmail.com', '2025-01-25'),
		('jiancpp', 'Jianna', 'Moraga', 'jia@gmail.com', '2014-12-13'),
		('piaya', 'Philomena', 'Punzalan', 'pia@gmail.com', '2008-06-07'),
		('pikachu123', 'Pika', 'Chu', 'pika123chu@gmail.com', '2020-10-09'),
		('marvelFan88', 'Marco', 'Santos', 'marco.santos@gmail.com', '2019-03-15'),
		('luna_star', 'Luna', 'Reyes', 'lunareyes@gmail.com', '2022-07-22'),
		('carlos_g', 'Carlos', 'Garcia', 'carlosg@gmail.com', '2018-11-30'),
		('annabanana', 'Anna', 'Flores', 'anna.flores@gmail.com', '2023-02-14'),
		('benito_m', 'Benjamin', 'Martinez', 'ben.martinez@gmail.com', '2021-09-18'),
		('maria_cruz', 'Maria', 'Cruz', 'maria.cruz@gmail.com', '2020-05-11'),
		('javier23', 'Javier', 'Ramos', 'javi.ramos@gmail.com', '2019-08-25'),
		('sophieTan', 'Sophie', 'Tan', 'sophie.tan@gmail.com', '2022-01-17'),
		('davidLim', 'David', 'Lim', 'david.lim@gmail.com', '2017-12-03'),
		('isabel_v', 'Isabel', 'Villanueva', 'isabel.v@gmail.com', '2023-06-30'),
		('rico_suave', 'Ricardo', 'Mendoza', 'rico.mendoza@gmail.com', '2016-09-14'),
		('clarissa88', 'Clarissa', 'Bautista', 'clarissa88@gmail.com', '2021-03-22'),
		('miguel_a', 'Miguel', 'Aquino', 'miguel.aquino@gmail.com', '2019-11-07'),
		('nicoleJ', 'Nicole', 'Jimenez', 'nicole.j@gmail.com', '2024-02-19'),
		('patrick_c', 'Patrick', 'Castro', 'patrick.castro@gmail.com', '2018-07-28'),
		('gabriela99', 'Gabriela', 'Torres', 'gabi.torres@gmail.com', '2022-09-05'),
		('rafael_m', 'Rafael', 'Marquez', 'rafael.m@gmail.com', '2020-12-11'),
		('carmen_l', 'Carmen', 'Lopez', 'carmen.lopez@gmail.com', '2017-04-16'),
		('antonio_r', 'Antonio', 'Rivera', 'antonio.r@gmail.com', '2023-08-09'),
		('valeria_s', 'Valeria', 'Santiago', 'valeria.s@gmail.com', '2021-11-23');

USE dbApp;

-- REFERENCE TABLES ===============================

INSERT INTO REF_Event_Type (Type_ID, Type_Name, Artist_Event_Only)
VALUES	(1, 'Concert', 1),
		(2, 'Fanmeet', 1),
		(3, 'Hi-Touch', 1),
		(4, 'Cupsleeve', 0),
		(5, 'Music Festival', 1),
		(6, 'Birthday Event', 0),
		(7, 'Anniversary Event', 0),
		(8, 'Viewing Party', 0),
		(9, 'KPOP Exhibit', 0),
		(10, 'Photo Zone', 0),
		(11, 'Showcase', 1);

INSERT INTO Location_Country (Location, Country)
VALUES	("Bocaue, Bulacan", "Philippines"),
		("Pasay City, Metro Manila", "Philippines"),
		("Taft Ave., Pasay City, Metro Manila", "Philippines"),
		("Quezon City, Metro Manila", "Philippines"),
		("Muntinlupa City, Metro Manila", "Philippines"),
		("Manila City, Metro Manila", "Philippines"),
		("Dasmariñas, Cavite", "Philippines"),
		("Bacoor, Cavite", "Philippines"),
		("Calamba, Laguna", "Philippines"),
		("Cebu City, Cebu", "Philippines");

-- ===============================================

INSERT INTO Venue (Venue_Name,Location,Capacity,Is_Seated)
VALUES  ("Philippine Arena","Bocaue, Bulacan",55000,1),
		("SM Mall of Asia Arena","Pasay City, Metro Manila",20000,1),
		("Smart Araneta Coliseum","Quezon City, Metro Manila",16500,1),
		("New Frontier Theater","Quezon City, Metro Manila",2385,1),
		("Huimang Café","Muntinlupa City, Metro Manila",NULL,0),
		("Chingu Dachi Cafe+","Manila City, Metro Manila",NULL,0),
		("Coffee Chapters","Taft Ave., Pasay City, Metro Manila",NULL,0),
		("Café Janggeum - SM North Edsa","Quezon City, Metro Manila",NULL,0),
		("Café Janggeum - SM City Dasma","Dasmariñas, Cavite",NULL,0),
		("Nineteen Degress - MOA","Pasay City, Metro Manila",NULL,0),
		("Coffee Grind Calamba City","Calamba, Laguna",NULL,0),
		("Villa Function Hall","Bacoor, Cavite",NULL,0),
		("SM Mall of Asia", "Pasay City, Metro Manila",NULL,0);

INSERT INTO Event (Event_ID, Event_Name, Venue_ID, Start_Date, End_Date, Start_Time, End_Time)
VALUES  (1,"BLACKPINK Comeback Tour",1,"2026-08-10","2026-08-10","20:00:00","0:00:00"),
		(2,"ENHYPEN Dunkin Donut Collab x Fanmeet",4,"2026-09-05","2026-09-05","14:00:00","16:30:00"),
		(3,"ZB1 Hi-Five Session",4,"2026-10-18","2026-10-18","11:00:00","13:00:00"),
		(4,"AKMU Birthday Cupsleeve Cafe",5,"2026-11-25","2026-11-25","10:00:00","17:00:00"),
		(5,"AESPA Artist Showcase",2,"2026-12-07","2026-12-07","18:30:00","22:30:00"),
		(6,"BLINKS United Rosé Birthday Event",6,"2026-02-11","2026-02-11","9:00:00","20:00:00"),
		(7,"Zerose Squad Anniversary Exhibit",12,"2026-07-10","2026-07-10","10:00:00","19:00:00"),
		(8,"WinRina 4ever Winter Cupsleeve Cafe",9,"2026-01-15","2026-01-15","9:30:00","18:30:00"),
		(9,"ENGENE-ers Sunghoon Birthday Cupsleeve",10,"2026-12-08","2026-12-08","10:00:00","20:00:00"),
		(10,"Pink Venom Club Jisoo Cupsleeve",11,"2026-01-03","2026-01-03","9:00:00","19:00:00"),
		(11,"MY Dreams Karina Birthday Cupsleeve",6,"2026-04-11","2026-04-11","10:00:00","18:00:00"),
		(12,"Tokki Squad Hanni Cupsleeve Event",8,"2026-10-06","2026-10-06","9:30:00","19:30:00"),
		(13,"AKKADEMY Chanhyuk Birthday Cupsleeve",9,"2026-09-12","2026-09-12","10:00:00","17:00:00"),
		(14,"Bunnies Forever Hyein Cupsleeve",10,"2026-04-21","2026-04-21","9:00:00","18:00:00"),
		(15,"ENGENE Nation Jungwon Cupsleeve",5,"2026-02-09","2026-02-12","10:00:00","19:00:00"),
		(16,"Zero Days Hanbin Birthday Cupsleeve",5,"2026-01-16","2026-01-18","9:30:00","20:00:00"),
		(17,"BP World Lisa Birthday Cupsleeve",8,"2026-03-27","2026-03-27","10:00:00","19:00:00"),
		(18,"Next Level Fans Winter Cupsleeve",9,"2026-02-14","2026-02-20","9:00:00","18:00:00"),
		(19,"WIZONE Forever Sakura Photozone",10,"2026-03-19","2026-03-19","10:00:00","19:00:00"),
		(20,"Bunny Camp Minji Birthday Exhbit",13,"2026-05-07","2026-05-07","9:30:00","19:30:00"),
		(21,"BLINK Paradise Jennie Cupsleeve",6,"2026-01-16","2026-01-16","10:00:00","20:00:00"),
		(22,"Vampire Lovers Heeseung Cupsleeve",8,"2026-10-15","2026-10-15","9:00:00","18:00:00"),
		(23,"ZB1 United Jiwoong Birthday Cupsleeve",9,"2026-12-14","2026-12-14","10:00:00","19:00:00"),
		(24,"Aespa Synk Ningning Cupsleeve",10,"2026-10-23","2026-10-23","9:30:00","18:30:00"),
		(25,"Suhyun & Chanhyuk Fans Anniversary Cupsleeve",11,"2026-04-19","2026-04-19","10:00:00","17:00:00"),
		(26,"IU Concert: Blooming in Blue",1,"2026-04-11","2026-04-12","20:00:00","0:00:00"),
		(27,"IZNA Anniversary Fanmeet",4,"2026-11-25","2026-11-25","17:00:00","22:00:00"),
		(28,"LISA: Lovesick Concert",3,"2026-01-15","2026-01-17","20:00:00","23:00:00"),
		(29,"SEVENTEEN Comeback Tour",1,"2027-01-23","2027-01-24","17:00:00","22:00:00"),
		(30,"ZB1 Summer in Manila Concert",2,"2026-02-28","2026-03-01","17:00:00","22:00:00"),
		(31,"KPOP Con: Manila Stage",3,"2025-12-12","2025-12-14","17:00:00","22:00:00"),
		(32,"Viewing Party",5,"2025-12-12","2025-12-12","17:00:00","18:00:00");
        
INSERT INTO Ticket_Tier(Tier_ID, Event_ID,Tier_Name,Price,Total_Quantity,Benefits,Is_Reserved_Seating)
VALUES	(1,1,"VIP Pit",15125,3900,"Early Entry, Sound Check Access",0),
		(2,1,"Lower Bowl A Premium",11550,3450,"Priority Entry, Exclusive Photocard",1),
		(3,1,"Lower Bowl A Regular",9900,6340,"Priority Entry, Exclusive Photocard",1),
		(4,1,"Lower Bowl B Premium",10250,4830,"Priority Entry, Exclusive Photocard",1),
		(5,1,"Lower Bowl B Regular",9150,10380,"Priority Entry, Exclusive Photocard",1),
		(6,1,"Upper Bowl Premium",6600,8100,"Standard Seating",1),
		(7,1,"Upper Bowl Regular",4950,13400,NULL,1),
		(8,2,"VIP Package",9900,1100,"Group Photo Raffle, Signed Poster",1),
		(9,2,"Loge Seating",6500,360,"Exclusive Merch Item",1),
		(10,2,"Balcony General Admission",2750,810,"Exclusive Merch Item",0),
		(11,3,"Hi-Touch VIP",8250,300,"Hi-Five Session, Signed Photocard",1),
		(12,3,"Patron",5500,300,"Exclusive Photocard",1),
		(13,3,"General Admission",3850,500,"Exclusive Photocard",0),
		(14,4,"Birthday Package",750,NULL,"Special Cupsleeve Set w/ Drink/Snack Voucher, Raffle Entry ",0),
		(15,4,"Cupsleeve Set",500,NULL,"Standard Cupsleeve Set w/ Drink/Snack Voucher",0),
		(16,5,"VIP Standing",14555,990,"Early Entry, Exclusive Lanyard and Ticket Holder",0),
		(17,5,"VIP Seated",12000,4480,"Early Entry, Exclusive Lanyard and Ticket Holder",1),
		(18,5,"Lower Box",9900,4160,"Priority Entry, Free Event Photocard",1),
		(19,5,"Upper Box A",6600,2520,"Priority Entry, Free Event Photocard",1),
		(20,5,"Upper Box B",4950,6020,"Free Event Photocard",0),
		(21,6,"Paid Entry",500,NULL,NULL,0),
		(22,7,"Paid Entry",300,NULL,NULL,0),
		(23,8,"Paid Entry",500,NULL,NULL,0),
		(24,9,"Paid Entry",500,NULL,NULL,0),
		(25,10,"Paid Entry",500,NULL,NULL,0),
		(26,11,"Paid Entry",500,NULL,NULL,0),
		(27,12,"Paid Entry",500,NULL,NULL,0),
		(28,13,"Paid Entry",500,NULL,NULL,0),
		(29,14,"Paid Entry",500,NULL,NULL,0),
		(30,15,"Paid Entry",500,NULL,NULL,0),
		(31,16,"Paid Entry",500,NULL,NULL,0),
		(32,17,"Paid Entry",500,NULL,NULL,0),
		(33,18,"Paid Entry",500,NULL,NULL,0),
		(34,19,"Paid Entry",500,NULL,NULL,0),
		(35,20,"Paid Entry",500,NULL,NULL,0),
		(36,21,"Paid Entry",500,NULL,NULL,0),
		(37,22,"Free Entry",0,NULL,NULL,0),
		(38,23,"Free Entry",0,NULL,NULL,0),
		(39,24,"Free Entry",0,NULL,NULL,0),
		(40,25,"Free Entry",0,NULL,NULL,0),
		(41,26,"VIP Seated",9500,1500,"Early Entry, Hi-Touch Session, ",1),
		(42,26,"Lower Bowl A Premium",7500,3450,"Early Entry, Sound Check Access",1),
		(43,26,"Lower Bowl A Regular",7300,6340,"Early Entry, Sound Check Access",1),
		(44,26,"Lower Bowl B Premium",5500,4830,NULL,1),
		(45,26,"Lower Bowl B Regular",4900,10380,NULL,1),
		(46,26,"Upper Bowl Premium",2250,8100,NULL,1),
		(47,26,"Upper Bowl Regular",1850,13400,NULL,1),
		(48,27,"Patron A",6000,300,"Hi Touch Session, Merch Giveaway",1),
		(49,27,"Patron B",5250,800,"Merch Giveaway",1),
		(50,27,"Patron C",4500,360,"Merch Giveaway",1),
		(51,27,"General Admission",1385,810,"Merch Giveaway",1),
		(52,28,"Day 1 - VIP Standing A",13500,850,"Priority Entry",0),
		(53,28,"Day 1 - VIP Standing B",9900,650,"Priority Entry",0),
		(54,28,"Day 1 - VIP Seated",10000,2100,"Priority Entry",1),
		(55,28,"Day 1 - Lower Box",7800,1550,"Early Entry",1),
		(56,28,"Day 1 - Upper Box",4550,5220,"Early Entry",1),
		(57,28,"Day 1 - General Admission",2000,2400,NULL,0),
		(58,29,"VIP Pit",18125,3900,"Early Entry, Sound Check Access",0),
		(59,29,"Lower Bowl A Premium",15550,3375,"Priority Entry, Exclusive Photocard",1),
		(60,29,"Lower Bowl A Regular",11000,4250,"Priority Entry, Exclusive Photocard",1),
		(61,29,"Lower Bowl B Premium",10250,4725,"Priority Entry, Exclusive Photocard",1),
		(62,29,"Lower Bowl B Regular",9150,9400,"Priority Entry, Exclusive Photocard",1),
		(63,29,"Upper Bowl Premium",6600,2260,"Standard Seating",1),
		(64,29,"Upper Bowl Regular",4950,7320,"Standard Seating",1),
		(65,30,"Day 1 - VIP Standing",12555,860,"Early Entry, Exclusive Lanyard and Ticket Holder",0),
		(66,30,"Day 1 - VIP Seated",10000,3895,"Early Entry, Exclusive Lanyard and Ticket Holder",1),
		(67,30,"Day 1 - Lower Box",9900,3990,"Priority Entry, Free Event Photocard",1),
		(68,30,"Day 1 - Upper Box A",6600,1970,"Priority Entry, Free Event Photocard",1),
		(69,30,"Day 1 - Upper Box B",4950,7185,"Free Event Photocard",1),
		(70,31,"Day 1 - VIP Standing A",8500,850,"Priority Entry",0),
		(71,31,"Day 1 - VIP Standing B",8000,650,"Priority Entry",0),
		(72,31,"Day 1 - VIP Seated",7000,3075,"Early Entry",1),
		(73,31,"Day 1 - Lower Box",5000,1550,"Early Entry",1),
		(74,31,"Day 1 - Upper Box",3550,5220,"Early Entry",1),
		(75,31,"Day 1 - General Admission",1200,2400,NULL,1),
		(76,31,"Day 2 - VIP Standing A",8500,850,"Priority Entry",0),
		(77,31,"Day 2 - VIP Standing B",8000,650,"Priority Entry",0),
		(78,31,"Day 2 - VIP Seated",7000,3075,"Early Entry",1),
		(79,31,"Day 2 - Lower Box",5000,1550,"Early Entry",1),
		(80,31,"Day 2 - Upper Box",3550,5220,"Early Entry",1),
		(81,31,"Day 2 - General Admission",1200,2400,NULL,1),
		(82,31,"Day 3 - VIP Standing A",8500,850,"Priority Entry",0),
		(83,31,"Day 3 - VIP Standing B",8000,650,"Priority Entry",0),
		(84,31,"Day 3 - VIP Seated",7000,3075,"Early Entry",1),
		(85,31,"Day 3 - Lower Box",5000,1550,"Early Entry",1),
		(86,31,"Day 3 - Upper Box",3550,5220,"Early Entry",1),
		(87,31,"Day 3 - General Admission",1200,2400,NULL,1),
		(88,28,"Day 2 - VIP Standing A",13500,850,"Priority Entry",0),
		(89,28,"Day 2 - VIP Standing B",9900,650,"Priority Entry",0),
		(90,28,"Day 2 - VIP Seated",10000,2100,"Priority Entry",1),
		(91,28,"Day 2 - Lower Box",7800,1550,"Early Entry",1),
		(92,28,"Day 2 - Upper Box",4550,5220,"Early Entry",1),
		(93,28,"Day 2 - General Admission",2000,2400,NULL,0),
		(94,28,'Day 3 - VIP Standing A',13500,850,'Priority Entry',0),
		(95,28,'Day 3 - VIP Standing B',9900,650,'Priority Entry',01),
		(96,28,'Day 3 - VIP Seated',10000,2100,'Priority Entry',1),
		(97,28,'Day 3 - Lower Box',7800,1550,'Early Entry',1),
		(98,28,'Day 3 - Upper Box',4550,5220,'Early Entry',1),
		(99,28,'Day 3 - General Admission',2000,2400,NULL,0),
		(100,30,"Day 2 - VIP Standing",12555,860,"Early Entry, Exclusive Lanyard and Ticket Holder",0),
		(101,30,"Day 2 - VIP Seated",10000,3895,"Early Entry, Exclusive Lanyard and Ticket Holder",1),
		(102,30,"Day 2 - Lower Box",9900,3990,"Priority Entry, Free Event Photocard",1),
		(103,30,"Day 2 - Upper Box A",6600,1970,"Priority Entry, Free Event Photocard",1),
		(104,30,"Day 2 - Upper Box B",4950,7185,"Free Event Photocard",1),
		(105,32,"Exclusive Viewing Party",0,7,"Free Event Photocard",0);

				
INSERT INTO Section(Section_ID,Venue_ID, Section_Name, Max_Capacity)
VALUES	(1,1,"101",500), 
		(2,1,"102",600),
		(3,1,"103",690),
		(4,1,"104",690),
		(5,1,"105",690),
		(6,1,"106",690),
		(7,1,"107",690),
		(8,1,"108",690),
		(9,1,"109",690),
		(10,1,"110",690),
		(11,1,"111",690),
		(12,1,"112",690),
		(13,1,"113",690),
		(14,1,"114",600),
		(15,1,"115",500),
		(16,1,"201",500),
		(17,1,"202",550),
		(18,1,"203",690),
		(19,1,"204",690),
		(20,1,"205",690),
		(21,1,"206",690),
		(22,1,"207",690),
		(23,1,"208",690),
		(24,1,"209",690),
		(25,1,"210",690),
		(26,1,"211",690),
		(27,1,"212",690),
		(28,1,"213",690),
		(29,1,"214",690),
		(30,1,"215",690),
		(31,1,"216",690),
		(32,1,"217",690),
		(33,1,"218",690),
		(34,1,"219",690),
		(35,1,"220",690),
		(36,1,"221",690),
		(37,1,"222",550),
		(38,1,"223",500),
		(39,1,"301",100),
		(40,1,"302",150),
		(41,1,"303",150),
		(42,1,"304",150),
		(43,1,"305",150),
		(44,1,"306",150),
		(45,1,"307",150),
		(46,1,"308",150),
		(47,1,"309",150),
		(48,1,"310",150),
		(49,1,"311",150),
		(50,1,"312",150),
		(51,1,"313",150),
		(52,1,"314",150),
		(53,1,"315",150),
		(54,1,"316",150),
		(55,1,"317",150),
		(56,1,"318",150),
		(57,1,"319",150),
		(58,1,"320",150),
		(59,1,"321",150),
		(60,1,"322",150),
		(61,1,"323",150),
		(62,1,"324",100),
		(63,1,"401",75),
		(64,1,"402",250),
		(65,1,"403",300),
		(66,1,"404",675),
		(67,1,"405",675),
		(68,1,"406",675),
		(69,1,"407",675),
		(70,1,"408",675),
		(71,1,"409",675),
		(72,1,"410",675),
		(73,1,"411",675),
		(74,1,"412",675),
		(75,1,"413",675),
		(76,1,"414",675),
		(77,1,"415",675),
		(78,1,"416",675),
		(79,1,"417",675),
		(80,1,"418",675),
		(81,1,"419",675),
		(82,1,"420",675),
		(83,1,"421",675),
		(84,1,"422",675),
		(85,1,"423",675),
		(86,1,"424",675),
		(87,1,"425",675),
		(88,1,"426",675),
		(89,1,"427",675),
		(90,1,"428",675),
		(91,1,"429",675),
		(92,1,"430",675),
		(93,1,"431",675),
		(94,1,"432",675),
		(95,1,"433",675),
		(96,1,"434",300),
		(97,1,"435",250),
		(98,1,"436",75),
		(99,1,"Zone A",350),
		(100,1,"Zone B",350),
		(101,1,"Zone C",350),
		(102,1,"Zone D",100),
		(103,1,"Zone E",350),
		(104,1,"Zone F",350),
		(105,1,"Zone G",350),
		(106,1,"Zone H",250),
		(107,1,"Zone I",250),
		(108,1,"Zone J",250),
		(109,1,"Zone K",200),
		(110,1,"Zone L",250),
		(111,1,"Zone M",250),
		(112,1,"Zone N",250),
		(113,2,"Floor A",495),
		(114,2,"Floor B",495),
		(115,2,"105",165),
		(116,2,"106",165),
		(117,2,"107",165),
		(118,2,"116",165),
		(119,2,"117",165),
		(120,2,"118",165),
		(121,2,"201",320),
		(122,2,"202",320),
		(123,2,"203",320),
		(124,2,"204",320),
		(125,2,"205",320),
		(126,2,"206",320),
		(127,2,"207",320),
		(128,2,"216",320),
		(129,2,"217",320),
		(130,2,"218",320),
		(131,2,"219",320),
		(132,2,"220",320),
		(133,2,"221",320),
		(134,2,"222",320),
		(135,2,"401",180),
		(136,2,"402",180),
		(137,2,"403",180),
		(138,2,"404",180),
		(139,2,"405",180),
		(140,2,"406",180),
		(141,2,"407",180),
		(142,2,"416",180),
		(143,2,"417",180),
		(144,2,"418",180),
		(145,2,"419",180),
		(146,2,"420",180),
		(147,2,"421",180),
		(148,2,"422",180),
		(149,2,"501",430),
		(150,2,"502",430),
		(151,2,"503",430),
		(152,2,"504",430),
		(153,2,"505",430),
		(154,2,"506",430),
		(155,2,"507",430),
		(156,2,"516",430),
		(157,2,"517",430),
		(158,2,"518",430),
		(159,2,"519",430),
		(160,2,"520",430),
		(161,2,"521",430),
		(162,2,"522",430),
		(163,4,"VVIP",300),
		(164,4,"VIP",800),
		(165,4,"Loge A",115),
		(166,4,"Loge B",130),
		(167,4,"Loge C",115),
		(168,4,"Balcony A",270),
		(169,4,"Balcony B",270),
		(170,4,"Balcony C",270),
		(171,3,"Floor A",750),
		(172,3,"Floor B",750),
		(173,3,"104",210),
		(174,3,"105",210),
		(175,3,"106",210),
		(176,3,"107",210),
		(177,3,"108",210),
		(178,3,"113",210),
		(179,3,"114",210),
		(180,3,"115",210),
		(181,3,"116",210),
		(182,3,"117",210),
		(183,3,"204",155),
		(184,3,"205",155),
		(185,3,"206",155),
		(186,3,"207",155),
		(187,3,"208",155),
		(188,3,"213",155),
		(189,3,"214",155),
		(190,3,"215",155),
		(191,3,"216",155),
		(192,3,"217",155),
		(193,3,"401",435),
		(194,3,"402",435),
		(195,3,"403",435),
		(196,3,"404",435),
		(197,3,"405",435),
		(198,3,"406",435),
		(199,3,"407",435),
		(200,3,"419",435),
		(201,3,"420",435),
		(202,3,"421",435),
		(203,3,"422",435),
		(204,3,"423",435),
		(205,3,"Gen. Ad.",2400);

-- Links

-- Event ID 1 (Tiers 1-7)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
    -- Seated
	(3,1), (3,2), (3,3), (3,4), (3,5), (2,6), (2,7), (2,8), (2,9), (2,10),
	(3,11), (3,12), (3,13), (3,14), (3,15),
	(5,16), (5,17), (5,18), (5,19), (5,20), (5,21), (5,22), (5,23),
	(4,24), (4,25), (4,26), (4,27), (4,28), (4,29), (4,30),
	(5,31), (5,32), (5,33), (5,34), (5,35), (5,36), (5,37), (5,38),
	(7,39), (7,40), (7,41), (7,42), (7,43), (7,44), (7,45), (7,46), (7,47), (7,48),
	(7,49), (7,50), (7,51), (7,52), (7,53), (7,54), (7,55), (7,56), (7,57), (7,58),
	(7,59), (7,60), (7,61), (7,62),
	(7,63), (7,64), (7,65), (7,66), (7,67), (7,68), (7,69), (7,70), (7,71), (7,72),
	(7,73), (7,74),
	(6,75), (6,76), (6,77), (6,78), (6,79), (6,80), (6,81), (6,82), (6,83), (6,84),
	(6,85), (6,86),
	(7,87), (7,88), (7,89), (7,90), (7,91), (7,92), (7,93), (7,94), (7,95), (7,96),
	(7,97), (7,98),
    -- Floor Standing
	(1,99), (1,100), (1,101), (1,102), (1,103), (1,104), (1,105), (1,106), (1,107), (1,108),
	(1,109), (1,110), (1,111), (1,112);

-- Event ID 2 (Tiers 8-10)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(8,163), (8,164),
	(9,165), (9,166), (9,167),
	(10,168), (10,169), (10,170);

-- Event ID 3 (Tiers 11-13)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(11,163),
	(12,164),
	(13,164);

-- Event ID 5 (Tiers 16-20)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(16,113), (16,114),
	(17,115), (17,116), (17,117), (17,118), (17,119), (17,120),
	(18,121), (18,122), (18,123), (18,124), (18,125), (18,126), (18,127),
	(18,128), (18,129), (18,130), (18,131), (18,132), (18,133), (18,134),
	(19,135), (19,136), (19,137), (19,138), (19,139), (19,140), (19,141),
	(19,142), (19,143), (19,144), (19,145), (19,146), (19,147), (19,148),
	(20,149), (20,150), (20,151), (20,152), (20,153), (20,154), (20,155),
	(20,156), (20,157), (20,158), (20,159), (20,160), (20,161), (20,162);

-- Event ID 26 (Tiers 41-47)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(43,1), (43,2), (43,3), (43,4), (43,5),
	(42,6), (42,7), (42,8), (42,9), (42,10),
	(43,11), (43,12), (43,13), (43,14), (43,15),
	(45,16), (45,17), (45,18), (45,19), (45,20), (45,21), (45,22), (45,23),
	(44,24), (44,25), (44,26), (44,27), (44,28), (44,29), (44,30),
	(45,31), (45,32), (45,33), (45,34), (45,35), (45,36), (45,37), (45,38),
	(47,63), (47,64), (47,65), (47,66), (47,67), (47,68), (47,69), (47,70), (47,71), (47,72),
	(47,73), (47,74),
	(46,75), (46,76), (46,77), (46,78), (46,79), (46,80), (46,81), (46,82), (46,83), (46,84),
	(46,85), (46,86),
	(47,87), (47,88), (47,89), (47,90), (47,91), (47,92), (47,93), (47,94), (47,95), (47,96),
	(47,97), (47,98),
	(41,99), (41,100), (41,101), (41,102), (41,103), (41,104), (41,105), (41,106), (41,107), (41,108),
	(41,109), (41,110), (41,111), (41,112);

-- Event ID 27 (Tiers 48-51)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(48,163),
	(49,164),
	(50,165), (50,166), (50,167),
	(51,168), (51,169), (51,170);

-- Event ID 28 
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
    -- Day One
	(52,171),
	(53,172),
	(54,173), (54,174), (54,175), (54,176), (54,177), (54,178),
	(54,179), (54,180), (54,181), (54,182),
	(55,183), (55,184), (55,185), (55,186), (55,187), (55,188), (55,189), (55,190),
	(55,191), (55,192),
	(56,193), (56,194), (56,195), (56,196), (56,197), (56,198), (56,199), (56,200),
	(56,201), (56,202), (56,203), (56,204),
	(57,205),

    -- Day Two
	(88,171),
	(89,172),
	(90,173), (90,174), (90,175), (90,176), (90,177), (90,178), 
    (90,179), (90,180), (90,181), (90,182),
	(91,183), (91,184), (91,185), (91,186), (91,187), (91,188), (91,189), (91,190), 
    (91,191), (91,192),
	(92,193), (92,194), (92,195), (92,196), (92,197), (92,198), (92,199), (92,200), 
    (92,201), (92,202), (92,203), (92,204),
	(93,205),

    -- Day Three
	(94,171), 
	(95,172),
	(96,173), (96,174), (96,175), (96,176), (96,177), 
    (96,178), (96,179), (96,180), (96,181), (96,182),
	(97,183), (97,184), (97,185), (97,186), (97,187), 
    (97,188), (97,189), (97,190), 
    (97,191), (97,192),
	(98,193), (98,194), (98,195), (98,196), (98,197),
    (98,198), (98,199), (98,200), (98,201), (98,202), (98,203), (98,204),
	(99,205);


-- Event ID 29 (Tiers 58-64)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(60,1), (60,2), (60,3), (60,4), (60,5),
	(59,6), (59,7), (59,8), (59,9), (59,10),
	(60,11), (60,12), (60,13), (60,14), (60,15),
	(62,16), (62,17), (62,18), (62,19), (62,20), (62,21), (62,22), (62,23),
	(61,24), (61,25), (61,26), (61,27), (61,28), (61,29), (61,30),
	(62,31), (62,32), (62,33), (62,34), (62,35), (62,36), (62,37), (62,38),
	(64,63), (64,64), (64,65), (64,66), (64,67), (64,68), (64,69), (64,70), (64,71), (64,72),
	(64,73), (64,74),
	(63,75), (63,76), (63,77), (63,78), (63,79), (63,80), (63,81), (63,82), (63,83), (63,84),
	(63,85), (63,86),
	(64,87), (64,88), (64,89), (64,90), (64,91), (64,92), (64,93), (64,94), (64,95), (64,96),
	(64,97), (64,98),
	(58,99), (58,100), (58,101), (58,102), (58,103), (58,104), (58,105), (58,106), (58,107), (58,108),
	(58,109), (58,110), (58,111), (58,112);

-- Event ID 30 (Tiers 65-69)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(65,113), (65,114),
	(66,115), (66,116), (66,117), (66,118), (66,119), (66,120),
	(67,121), (67,122), (67,123), (67,124), (67,125), (67,126), (67,127),
	(67,128), (67,129), (67,130), (67,131), (67,132), (67,133), (67,134),
	(68,135), (68,136), (68,137), (68,138), (68,139), (68,140), (68,141),
	(68,142), (68,143), (68,144), (68,145), (68,146), (68,147), (68,148),
	(69,149), (69,150), (69,151), (69,152), (69,153), (69,154), (69,155),
	(69,156), (69,157), (69,158), (69,159), (69,160), (69,161), (69,162),

	(100,113), (100,114),
	(101,115), (101,116), (101,117), (101,118), (101,119), (101,120),
	(102,121), (102,122), (102,123), (102,124), (102,125), (102,126), (102,127),
	(102,128), (102,129), (102,130), (102,131), (102,132), (102,133), (102,134),
	(103,135), (103,136), (102,137), (103,138), (103,139), (103,140), (103,141),
	(103,142), (103,143), (103,144), (103,145), (103,146), (103,147), (103,148),
	(104,149), (104,150), (104,151), (104,152), (104,153), (104,154), (104,155),
	(104,156), (104,157), (104,158), (104,159), (104,160), (104,161), (104,162);
    

-- Event ID 31 (Tiers 70-87)
INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES
	(70,171),
	(71,172),
	(72,173), (72,174), (72,175), (72,176), (72,177), (72,178),
	(72,179), (72,180), (72,181), (72,182),
	(73,183), (73,184), (73,185), (73,186), (73,187), (73,188), (73,189), (73,190),
	(73,191), (73,192),
	(74,193), (74,194), (74,195), (74,196), (74,197), (74,198), (74,199), (74,200),
	(74,201), (74,202), (74,203), (74,204),
	(75,205),

    (76,171),
	(77,172),
	(78,173), (78,174), (78,175), (78,176), (78,177), (78,178),
	(78,179), (78,180), (78,181), (78,182),
	(79,183), (79,184), (79,185), (79,186), (79,187), (79,188), (79,189), (79,190),
	(79,191), (79,192),
	(80,193), (80,194), (80,195), (80,196), (80,197), (80,198), (80,199), (80,200),
	(80,201), (80,202), (80,203), (80,204),
	(81,205),

	(82,171),
	(83,172),
	(84,173), (84,174), (84,175), (84,176), (84,177), (84,178),
	(84,179), (84,180), (84,181), (84,182),
	(85,183), (85,184), (85,185), (85,186), (85,187), (85,188), (85,189), (85,190),
	(85,191), (85,192),
	(86,193), (86,194), (86,195), (86,196), (86,197), (86,198), (86,199), (86,200),
	(86,201), (86,202), (86,203), (86,204),
	(87,205);


INSERT INTO LINK_Event_Type (Event_ID, Type_ID)
VALUES
-- Event 1: "BLACKPINK Comeback Tour" -> "Concert" (ID 1)
(1, 1),

-- Event 2: "ENHYPEN Dunkin Donut Collab x Fanmeet" -> "Fanmeet" (ID 2), "Hi-Touch" (ID 3)
(2, 2), (2, 3),

-- Event 3: "ZB1 Hi-Five Session" -> "Hi-Touch" (ID 3)
(3, 3),

-- Event 4: AKMU Birthday Cupsleeve Cafe
(4, 4), (4, 6),

-- Event 5: AESPA Artist Showcase
(5, 11),

-- Event 6: BLINKS United Rosé Birthday Event
(6, 6), (6, 10),

-- Event: Zerose Squad Anniversary Exhibit
(7, 7), (7, 9),

-- WinRina 4ever Winter Cupsleeve Cafe
(8, 4),

-- ENGENE-ers Sunghoon Birthday Cupsleeve
(9, 6), (9, 4),

-- Pink Venom Club Jisoo Cupsleeve
(10, 4),

-- MY Dreams Karina Birthday Cupsleeve
(11, 6), (11, 4),

-- Tokki Squad Hanni Cupsleeve Event
(12, 4),

-- AKKADEMY Chanhyuk Birthday Cupsleeve
(13, 6), (13, 4),

-- Bunnies Forever Hyein Cupsleeve
(14, 4), 

-- ENGENE Nation Jungwon Cupsleeve
(15, 4),

-- Zero Days Hanbin Birthday Cupsleeve
(16, 6), (16, 4),

-- BP World Lisa Birthday Cupsleeve
(17, 6), (17, 4),

-- Next Level Fans Winter Cupsleeve
(18, 6), (18, 4),

-- WIZONE Forever Sakura Photozone
(19, 10), 

-- Bunny Camp Minji Birthday Exhibit
(20, 6), (20, 9),

-- BLINK Paradise Jennie Cupsleeve
(21, 4),

-- Vampire Lovers Heeseung Cupsleeve
(22, 4),

-- ZB1 United Jiwoong Birthday Cupsleeve
(23, 6), (23, 4),

-- Aespa Synk Ningning Cupsleeve
(24, 4),

-- Suhyun & Chanhyuk Fans Anniversary Cupsleeve
(25, 6), (25, 4),

-- Event 26: "IU Concert: Blooming in Blue" -> "Concert" (ID 1), "Hi-Touch" (ID 3)
(26, 1), (26, 3),

-- Event 27: "IZNA Anniversary Fanmeet" -> "Fanmeet" (ID 2), "Hi-Touch" (ID 3)
(27, 2), (27, 3),

-- Event 28: "LISA: Lovesick Concert" -> "Concert" (ID 1)
(28, 1),

-- Event 29: "SEVENTEEN Comeback Tour" -> "Concert" (ID 1)
(29, 1),

-- Event 30: "ZB1 Summer in Manila Concert" -> "Concert" (ID 1)
(30, 1),

-- Event 31: "SB19 Asia Stage: Manila" -> "Concert" (ID 1)
(31, 1);


INSERT INTO Ticket_Purchase (Ticket_ID, Fan_ID, Event_ID, Tier_ID, Seat_ID, Purchase_Date)
VALUES
    (1,1,30,67,56212,'2025-11-16 23:45:53'),
    (2,1,30,67,56213,'2025-11-16 23:45:53'),
    (3,1,30,67,56214,'2025-11-16 23:45:53'),
    (4,1,30,67,56242,'2025-11-16 23:45:53'),
    (5,1,30,67,56243,'2025-11-16 23:45:53'),
    (6,1,30,67,56244,'2025-11-16 23:45:53'),
    (7,1,30,67,56245,'2025-11-16 23:45:53'),
    (8,1,30,67,56273,'2025-11-16 23:45:53'),
    (9,1,30,67,56274,'2025-11-16 23:45:53'),
    (10,1,30,67,56275,'2025-11-16 23:45:53'),
    (11,1,30,102,56215,'2025-11-16 23:46:11'),
    (12,1,30,102,56216,'2025-11-16 23:46:11'),
    (13,1,30,102,56217,'2025-11-16 23:46:12'),
    (14,1,30,102,56218,'2025-11-16 23:46:12'),
    (15,1,30,102,56246,'2025-11-16 23:46:12'),
    (16,1,30,102,56247,'2025-11-16 23:46:12'),
    (17,1,30,102,56276,'2025-11-16 23:46:12'),
    (18,1,30,102,56277,'2025-11-16 23:46:12'),
    (19,1,30,102,56306,'2025-11-16 23:46:12'),
    (20,1,30,102,56307,'2025-11-16 23:46:12'),
    (21,1,11,26,NULL,'2025-11-16 23:47:01'),
    (22,1,11,26,NULL,'2025-11-16 23:47:01'),
    (23,1,11,26,NULL,'2025-11-16 23:47:01'),
    (24,1,11,26,NULL,'2025-11-16 23:47:01'),
    (25,1,11,26,NULL,'2025-11-16 23:47:01'),
    (26,1,11,26,NULL,'2025-11-16 23:47:01'),
    (27,1,11,26,NULL,'2025-11-16 23:47:01'),
    (28,1,11,26,NULL,'2025-11-16 23:47:01'),
    (29,1,11,26,NULL,'2025-11-16 23:47:01'),
    (30,1,11,26,NULL,'2025-11-16 23:47:01'),
    (31,1,5,17,54900,'2025-11-16 23:47:41'),
    (32,1,5,17,54901,'2025-11-16 23:47:41'),
    (33,1,5,17,54902,'2025-11-16 23:47:41'),
    (34,1,5,17,54903,'2025-11-16 23:47:41'),
    (35,1,5,17,54904,'2025-11-16 23:47:41'),
    (36,1,5,17,54930,'2025-11-16 23:47:41'),
    (37,1,5,17,54931,'2025-11-16 23:47:41'),
    (38,1,5,17,54932,'2025-11-16 23:47:41'),
    (39,1,5,17,54933,'2025-11-16 23:47:41'),
    (40,1,5,17,54934,'2025-11-16 23:47:41'),
    (41,2,31,73,75093,'2025-11-16 23:48:37'),
    (42,2,31,73,75094,'2025-11-16 23:48:37'),
    (43,2,31,73,75095,'2025-11-16 23:48:37'),
    (44,2,31,73,75096,'2025-11-16 23:48:37'),
    (45,2,31,73,75123,'2025-11-16 23:48:37'),
    (46,2,31,73,75124,'2025-11-16 23:48:37'),
    (47,2,31,73,75125,'2025-11-16 23:48:37'),
    (48,2,5,17,54905,'2025-11-16 23:49:19'),
    (49,2,5,17,54906,'2025-11-16 23:49:19'),
    (50,2,5,17,54907,'2025-11-16 23:49:19'),
    (51,2,5,17,54935,'2025-11-16 23:49:19'),
    (52,2,5,17,54936,'2025-11-16 23:49:19'),
    (53,2,5,17,54937,'2025-11-16 23:49:19'),
    (54,2,5,17,54938,'2025-11-16 23:49:19'),
    (55,2,5,17,54966,'2025-11-16 23:49:19'),
    (56,2,5,17,54967,'2025-11-16 23:49:19'),
    (57,2,5,17,54968,'2025-11-16 23:49:19'),
    (58,4,29,59,3903,'2025-11-16 23:50:14'),
    (59,4,29,59,3904,'2025-11-16 23:50:14'),
    (60,4,29,59,3905,'2025-11-16 23:50:14'),
    (61,4,29,59,3906,'2025-11-16 23:50:14'),
    (62,4,29,59,3935,'2025-11-16 23:50:14'),
    (63,4,29,59,3936,'2025-11-16 23:50:14'),
    (64,4,19,34,NULL,'2025-11-16 23:50:30'),
    (65,4,19,34,NULL,'2025-11-16 23:50:30'),
    (66,4,19,34,NULL,'2025-11-16 23:50:30'),
    (67,4,19,34,NULL,'2025-11-16 23:50:30'),
    (68,4,19,34,NULL,'2025-11-16 23:50:30'),
    (69,4,19,34,NULL,'2025-11-16 23:50:30'),
    (70,4,19,34,NULL,'2025-11-16 23:50:30'),
    (71,4,19,34,NULL,'2025-11-16 23:50:30'),
    (72,4,19,34,NULL,'2025-11-16 23:50:30'),
    (73,4,19,34,NULL,'2025-11-16 23:50:30'),
    (74,4,28,57,NULL,'2025-11-16 23:50:50'),
    (75,4,28,57,NULL,'2025-11-16 23:50:50'),
    (76,4,28,57,NULL,'2025-11-16 23:50:50'),
    (77,4,28,57,NULL,'2025-11-16 23:50:50'),
    (78,4,28,57,NULL,'2025-11-16 23:50:50'),
    (79,4,28,57,NULL,'2025-11-16 23:50:50'),
    (80,4,28,57,NULL,'2025-11-16 23:50:50'),
    (81,4,28,57,NULL,'2025-11-16 23:50:50'),
    (82,4,28,57,NULL,'2025-11-16 23:50:50'),
    (83,4,28,57,NULL,'2025-11-16 23:50:50'),
    (84,5,30,66,55067,'2025-11-16 23:52:42'),
    (85,5,30,66,55068,'2025-11-16 23:52:42'),
    (86,5,30,66,55069,'2025-11-16 23:52:42'),
    (87,5,30,66,55070,'2025-11-16 23:52:42'),
    (88,5,30,66,55097,'2025-11-16 23:52:42'),
    (89,5,30,66,55098,'2025-11-16 23:52:42'),
    (90,5,30,66,55136,'2025-11-16 23:52:42'),
    (91,5,30,66,55137,'2025-11-16 23:52:42'),
    (92,5,30,66,55138,'2025-11-16 23:52:42'),
    (93,5,30,66,55139,'2025-11-16 23:52:42'),
    (94,5,26,41,50010,'2025-11-16 23:53:21'),
    (95,5,26,41,50011,'2025-11-16 23:53:21'),
    (96,5,26,41,50012,'2025-11-16 23:53:21'),
    (97,5,26,41,50050,'2025-11-16 23:53:21'),
    (98,5,26,41,50051,'2025-11-16 23:53:21'),
    (99,5,26,41,50082,'2025-11-16 23:53:21'),
    (100,5,26,41,50083,'2025-11-16 23:53:21'),
    (101,5,26,41,50105,'2025-11-16 23:53:21'),
    (102,5,26,41,50106,'2025-11-16 23:53:21'),
    (103,5,26,41,50107,'2025-11-16 23:53:21'),
    (104,5,10,25,NULL,'2025-11-16 23:54:05'),
    (105,5,10,25,NULL,'2025-11-16 23:54:05'),
    (106,5,10,25,NULL,'2025-11-16 23:54:05'),
    (107,5,10,25,NULL,'2025-11-16 23:54:05'),
    (108,5,10,25,NULL,'2025-11-16 23:54:05'),
    (109,5,10,25,NULL,'2025-11-16 23:54:05'),
    (110,5,4,14,NULL,'2025-11-16 23:54:29'),
    (111,5,4,14,NULL,'2025-11-16 23:54:29'),
    (112,5,4,14,NULL,'2025-11-16 23:54:29'),
    (113,5,4,14,NULL,'2025-11-16 23:54:29'),
    (114,5,7,22,NULL,'2025-11-16 23:54:49'),
    (115,5,7,22,NULL,'2025-11-16 23:54:49'),
    (116,5,7,22,NULL,'2025-11-16 23:54:49'),
    (117,5,7,22,NULL,'2025-11-16 23:54:49'),
    (118,5,7,22,NULL,'2025-11-16 23:54:49'),
    (119,6,28,57,NULL,'2025-11-16 23:55:54'),
    (120,6,28,57,NULL,'2025-11-16 23:55:54'),
    (121,6,28,57,NULL,'2025-11-16 23:55:54'),
    (122,6,28,57,NULL,'2025-11-16 23:55:54'),
    (123,6,28,57,NULL,'2025-11-16 23:55:54'),
    (124,6,28,57,NULL,'2025-11-16 23:55:54'),
    (125,6,28,57,NULL,'2025-11-16 23:55:55'),
    (126,6,28,57,NULL,'2025-11-16 23:55:55'),
    (127,6,28,57,NULL,'2025-11-16 23:55:55'),
    (128,6,28,57,NULL,'2025-11-16 23:55:55'),
    (129,6,28,54,73103,'2025-11-16 23:56:21'),
    (130,6,28,54,73104,'2025-11-16 23:56:21'),
    (131,6,28,54,73105,'2025-11-16 23:56:21'),
    (132,6,28,54,73106,'2025-11-16 23:56:21'),
    (133,6,28,54,73132,'2025-11-16 23:56:21'),
    (134,6,28,54,73133,'2025-11-16 23:56:21'),
    (135,6,28,54,73134,'2025-11-16 23:56:21'),
    (136,6,28,54,73163,'2025-11-16 23:56:21'),
    (137,6,28,54,73201,'2025-11-16 23:56:21'),
    (138,6,28,54,73202,'2025-11-16 23:56:21'),
    (139,6,28,55,75246,'2025-11-16 23:56:43'),
    (140,6,28,55,75247,'2025-11-16 23:56:43'),
    (141,6,28,55,75248,'2025-11-16 23:56:43'),
    (142,6,28,55,75249,'2025-11-16 23:56:43'),
    (143,6,28,55,75276,'2025-11-16 23:56:43'),
    (144,6,28,55,75277,'2025-11-16 23:56:43'),
    (145,6,28,55,75278,'2025-11-16 23:56:43'),
    -- (146,6,28,52,71183,'2025-11-16 23:58:07'),
    -- (147,6,28,52,71184,'2025-11-16 23:58:07'),
    -- (148,6,28,52,71185,'2025-11-16 23:58:07'),
    -- (149,6,28,52,71186,'2025-11-16 23:58:07'),
    (150,7,29,59,3938,'2025-11-17 00:00:00'),
    (151,7,29,59,3939,'2025-11-17 00:00:01'),
    (152,7,29,59,3940,'2025-11-17 00:00:01'),
    (153,7,29,59,3941,'2025-11-17 00:00:01'),
    (154,7,29,59,3968,'2025-11-17 00:00:01'),
    (155,7,29,59,3969,'2025-11-17 00:00:01'),
    (156,7,29,59,3970,'2025-11-17 00:00:01'),
    (157,7,31,72,72898,'2025-11-17 00:00:40'),
    (158,7,31,72,72899,'2025-11-17 00:00:40'),
    (159,7,31,72,72900,'2025-11-17 00:00:40'),
    (160,7,31,72,72901,'2025-11-17 00:00:40'),
    (161,7,31,72,72926,'2025-11-17 00:00:40'),
    (162,7,31,72,72954,'2025-11-17 00:00:40'),
    (163,7,31,72,72955,'2025-11-17 00:00:40'),
    (164,7,31,72,72956,'2025-11-17 00:00:40'),
    (165,7,31,72,72984,'2025-11-17 00:00:40'),
    (166,7,31,72,72985,'2025-11-17 00:00:40'),
    (167,7,1,6,38592,'2025-11-17 00:01:07'),
    (168,7,1,6,38593,'2025-11-17 00:01:07'),
    (169,7,1,6,38594,'2025-11-17 00:01:08'),
    (170,7,1,6,38618,'2025-11-17 00:01:08'),
    (171,7,1,6,38619,'2025-11-17 00:01:08'),
    (172,7,1,6,38620,'2025-11-17 00:01:08'),
    (173,7,1,6,38649,'2025-11-17 00:01:08'),
    (174,7,1,6,38650,'2025-11-17 00:01:08'),
    (175,7,3,11,68912,'2025-11-17 00:02:02'),
    (176,7,3,11,68913,'2025-11-17 00:02:02'),
    (177,7,3,11,68914,'2025-11-17 00:02:02'),
    (178,7,3,11,68915,'2025-11-17 00:02:02'),
    (179,7,3,12,69211,'2025-11-17 00:02:28'),
    (180,7,3,12,69212,'2025-11-17 00:02:28'),
    (181,7,3,12,69213,'2025-11-17 00:02:28'),
    (182,7,3,12,69214,'2025-11-17 00:02:28'),
    (183,7,3,12,69215,'2025-11-17 00:02:28'),
    (184,7,3,12,69216,'2025-11-17 00:02:28'),
    (185,7,3,13,NULL,'2025-11-17 00:02:39'),
    (186,7,3,13,NULL,'2025-11-17 00:02:39'),
    (187,7,3,13,NULL,'2025-11-17 00:02:39'),
    (188,7,3,13,NULL,'2025-11-17 00:02:39'),
    (189,7,3,13,NULL,'2025-11-17 00:02:39'),
    (190,7,3,13,NULL,'2025-11-17 00:02:39'),
    (191,7,3,13,NULL,'2025-11-17 00:02:39'),
    (192,8,31,74,78506,'2025-11-17 00:04:19'),
    (193,8,31,74,78507,'2025-11-17 00:04:19'),
    (194,8,31,74,78508,'2025-11-17 00:04:19'),
    (195,8,31,74,78509,'2025-11-17 00:04:19'),
    (196,8,31,74,78510,'2025-11-17 00:04:19'),
    (197,8,31,74,78511,'2025-11-17 00:04:19'),
    (198,8,31,74,78512,'2025-11-17 00:04:19'),
    (199,8,31,74,78513,'2025-11-17 00:04:19'),
    (200,8,31,74,78514,'2025-11-17 00:04:19'),
    (201,8,31,74,78515,'2025-11-17 00:04:19'),
    (202,8,31,72,73099,'2025-11-17 00:04:43'),
    (203,8,31,72,73100,'2025-11-17 00:04:43'),
    (204,8,31,72,73101,'2025-11-17 00:04:43'),
    (205,8,31,72,73102,'2025-11-17 00:04:43'),
    (206,8,31,72,73103,'2025-11-17 00:04:43'),
    (207,8,31,72,73104,'2025-11-17 00:04:43'),
    (208,8,31,72,73105,'2025-11-17 00:04:43'),
    (209,8,31,72,73106,'2025-11-17 00:04:43'),
    (210,8,31,72,73107,'2025-11-17 00:04:43'),
    (211,8,31,72,73108,'2025-11-17 00:04:43'),
    (212,8,31,72,72886,'2025-11-17 00:04:59'),
    (213,8,31,72,72887,'2025-11-17 00:04:59'),
    (214,8,31,72,72888,'2025-11-17 00:04:59'),
    (215,8,31,72,72889,'2025-11-17 00:04:59'),
    (216,8,31,72,72676,'2025-11-17 00:05:24'),
    (217,8,31,72,72677,'2025-11-17 00:05:24'),
    (218,8,31,72,72678,'2025-11-17 00:05:24'),
    (219,8,31,72,72679,'2025-11-17 00:05:24'),
    (220,8,31,72,72680,'2025-11-17 00:05:24'),
    (221,8,31,72,72681,'2025-11-17 00:05:24'),
    (222,8,31,72,72682,'2025-11-17 00:05:24'),
    (223,8,31,72,72683,'2025-11-17 00:05:24'),
    (224,8,31,72,72684,'2025-11-17 00:05:24'),
    (225,8,10,25,NULL,'2025-11-17 00:05:42'),
    (226,8,10,25,NULL,'2025-11-17 00:05:42'),
    (227,8,10,25,NULL,'2025-11-17 00:05:42'),
    (228,8,10,25,NULL,'2025-11-17 00:05:42'),
    (229,8,10,25,NULL,'2025-11-17 00:05:42'),
    (230,8,10,25,NULL,'2025-11-17 00:05:42'),
    (231,8,10,25,NULL,'2025-11-17 00:05:42'),
    (232,8,10,25,NULL,'2025-11-17 00:05:42'),
    (233,8,10,25,NULL,'2025-11-17 00:05:42'),
    (234,8,10,25,NULL,'2025-11-17 00:05:42'),
    (235,8,2,10,NULL,'2025-11-17 00:06:44'),
    (236,8,2,10,NULL,'2025-11-17 00:06:44'),
    (237,8,2,10,NULL,'2025-11-17 00:06:44'),
    (238,8,2,10,NULL,'2025-11-17 00:06:44'),
    (239,8,2,10,NULL,'2025-11-17 00:06:44'),
    (240,8,2,10,NULL,'2025-11-17 00:06:44'),
    (241,8,2,10,NULL,'2025-11-17 00:06:44'),
    (242,9,6,21,NULL,'2025-11-17 00:07:41'),
    (243,9,6,21,NULL,'2025-11-17 00:07:41'),
    (244,9,6,21,NULL,'2025-11-17 00:07:41'),
    (245,9,6,21,NULL,'2025-11-17 00:07:41'),
    (246,9,6,21,NULL,'2025-11-17 00:07:41'),
    (247,9,31,74,78941,'2025-11-17 00:08:23'),
    (248,9,31,74,78942,'2025-11-17 00:08:23'),
    (249,9,31,74,78970,'2025-11-17 00:08:23'),
    (250,9,31,74,78971,'2025-11-17 00:08:23'),
    (251,9,31,74,78998,'2025-11-17 00:08:23'),
    (252,9,31,74,78999,'2025-11-17 00:08:23'),
    (253,9,31,74,79002,'2025-11-17 00:08:23'),
    (254,9,31,74,79003,'2025-11-17 00:08:23'),
    (255,9,31,74,79004,'2025-11-17 00:08:23'),
    (256,10,8,23,NULL,'2025-11-17 00:09:40'),
    (257,10,8,23,NULL,'2025-11-17 00:09:40'),
    (258,10,8,23,NULL,'2025-11-17 00:09:40'),
    (259,10,8,23,NULL,'2025-11-17 00:09:40'),
    (260,10,8,23,NULL,'2025-11-17 00:09:40'),
    (261,11,9,24,NULL,'2025-11-17 00:10:35'),
    (262,11,9,24,NULL,'2025-11-17 00:10:35'),
    (263,11,9,24,NULL,'2025-11-17 00:10:35'),
    (264,11,9,24,NULL,'2025-11-17 00:10:35'),
    (265,11,31,70,NULL,'2025-11-17 00:10:52'),
    (266,11,31,70,NULL,'2025-11-17 00:10:52'),
    (267,11,31,70,NULL,'2025-11-17 00:10:52'),
    (268,11,31,70,NULL,'2025-11-17 00:10:52'),
    (269,11,31,70,NULL,'2025-11-17 00:10:52'),
    (270,11,31,70,NULL,'2025-11-17 00:10:52'),
    (271,11,31,70,NULL,'2025-11-17 00:10:52'),
    (272,11,31,70,NULL,'2025-11-17 00:10:52'),
    (273,11,31,70,NULL,'2025-11-17 00:10:52'),
    (274,11,31,70,NULL,'2025-11-17 00:10:52'),
    (275,12,30,68,61993,'2025-11-17 00:11:48'),
    (276,12,30,68,61994,'2025-11-17 00:11:48'),
    (277,12,30,68,61995,'2025-11-17 00:11:48'),
    (278,12,30,68,62023,'2025-11-17 00:11:48'),
    (279,12,30,68,62024,'2025-11-17 00:11:48'),
    (280,12,30,68,62090,'2025-11-17 00:11:48'),
    (281,12,30,68,62091,'2025-11-17 00:11:48'),
    (282,12,30,68,62092,'2025-11-17 00:11:48'),
    (283,12,30,68,62093,'2025-11-17 00:11:48'),
    (284,12,30,68,62094,'2025-11-17 00:11:48'),
    (285,13,1,3,8704,'2025-11-17 00:12:28'),
    (286,13,1,3,8714,'2025-11-17 00:12:28'),
    (287,13,1,3,8715,'2025-11-17 00:12:28'),
    (288,13,1,3,8716,'2025-11-17 00:12:28'),
    (289,13,1,3,8738,'2025-11-17 00:12:28'),
    (290,13,1,3,8739,'2025-11-17 00:12:28'),
    (291,13,1,3,8818,'2025-11-17 00:12:28'),
    (292,13,1,3,8819,'2025-11-17 00:12:28'),
    (293,14,3,11,68945,'2025-11-17 00:13:06'),
    (294,14,3,11,68946,'2025-11-17 00:13:06'),
    (295,14,3,11,68947,'2025-11-17 00:13:06'),
    (296,14,3,11,68948,'2025-11-17 00:13:06'),
    (297,14,3,11,68949,'2025-11-17 00:13:06');

-- 1. MANAGER TABLE (Parent)
INSERT INTO Manager (Manager_ID, Manager_Name, Contact_Num, Contact_Email, Agency) VALUES
(1, 'Kim Min-jun', '01012345678', 'm.kim@ygmail.com', 'YG'),
(2, 'Sejin', '01098765432', 's.jin@gmail.com', 'Belift Lab'),
(3, 'Park Seo-joon', '01022446688', 's.park@wakeone.com', 'WakeOne'),
(4, 'Choi Eun-woo', '01013572468', 'e.choi@ygmail.com', 'YG'),
(5, 'Jung Ha-yoon', '01055117733', 'h.jung@smtown.com', 'SM Entertainment'),
(6, 'Kang Ji-hyun', '01086420975', 'j.kang@ador.world', 'ADOR'),
(7, 'Han Sung-min', '01031415926', 's.han@offtherecord.co.kr', 'OTR Entertainment');

-- 2. ARTIST TABLE (Parent, references Manager)
INSERT INTO Artist (Artist_ID, Manager_ID, Artist_Name, Activity_Status, Debut_Date) VALUES
(1, 1, 'BlackPink', 'Active', '2016-08-08'),
(2, 2, 'Enhypen', 'Active', '2020-11-30'),
(3, 3, 'Zerobaseone', 'Active', '2023-07-10'),
(4, 4, 'AKMU', 'Active', '2014-04-07'),
(5, 5, 'Aespa', 'Active', '2020-11-27'),
(6, 6, 'New Jeans', 'Hiatus', '2022-07-22'),
(7, 7, 'Iz*One', 'Inactive', '2018-10-29'),
(8, NULL, 'IU', 'Active', '2008-09-18'),
(9, NULL, 'IZNA', 'Active', '2024-11-25'),
(10, NULL, 'SEVENTEEN', 'Active', '2015-05-26'),
(11, NULL, 'UNIS', 'Active', '2024-03-07');

-- 3. MEMBER TABLE (Child, references Artist)
INSERT INTO Member (Member_ID, Artist_ID, Member_Name, Activity_Status, Birth_Date) VALUES
(1, 1, 'Kim Ji-soo', 'Active', '1995-01-03'),
(2, 1, 'Jennie Kim', 'Active', '1996-01-16'),
(3, 1, 'Rosé Park', 'Active', '1997-02-11'),
(4, 1, 'Lisa Manoban', 'Active', '1997-03-27'),
(5, 2, 'Yang Jung-won', 'Active', '2004-02-09'),
(6, 2, 'Lee Hee-seung', 'Active', '2001-10-15'),
(7, 2, 'Jay Park', 'Active', '2002-04-20'),
(8, 2, 'Jake Sim', 'Active', '2002-11-15'),
(9, 2, 'Park Sung-hoon', 'Active', '2002-12-08'),
(10, 2, 'Kim Sun-oo', 'Active', '2003-06-24'),
(11, 2, 'Ni-ki', 'Active', '2005-12-09'),
(12, 3, 'Kim Ji-woong', 'Active', '1998-12-14'),
(13, 3, 'Zhang Hao', 'Active', '2000-07-25'),
(14, 3, 'Sung Han-bin', 'Active', '2001-06-13'),
(15, 3, 'Seok Matthew', 'Active', '2002-05-28'),
(16, 3, 'Kim Tae-rae', 'Active', '2002-07-14'),
(17, 3, 'Ricky (Shen Quanrui)', 'Active', '2004-05-20'),
(18, 3, 'Kim Gyu-vin', 'Active', '2004-08-30'),
(19, 3, 'Park Gun-wook', 'Active', '2005-01-10'),
(20, 3, 'Han Yu-jin', 'Active', '2007-03-20'),
(21, 4, 'Lee Chan-hyuk', 'Active', '1996-09-12'),
(22, 4, 'Lee Su-hyun', 'Active', '1999-05-04'),
(23, 5, 'Karina (Yu Ji-min)', 'Active', '2000-04-11'),
(24, 5, 'Giselle (Uchinaga Eri)', 'Active', '2000-10-30'),
(25, 5, 'Winter (Kim Min-jeong)', 'Active', '2001-01-01'),
(26, 5, 'Ningning (Ning Yizhuo)', 'Active', '2002-10-23'),
(27, 6, 'Minji (Kim Min-ji)', 'Hiatus', '2004-05-07'),
(28, 6, 'Hanni (Pham Ngoc Han)', 'Hiatus', '2004-10-06'),
(29, 6, 'Danielle (Mo Ji-hye)', 'Hiatus', '2005-04-11'),
(30, 6, 'Haerin (Kang Hae-rin)', 'Hiatus', '2006-05-15'),
(31, 6, 'Hyein (Lee Hye-in)', 'Hiatus', '2008-04-21'),
(32, 7, 'Kwon Eun-bi', 'Inactive', '1995-09-27'),
(33, 7, 'Sakura Miyawaki', 'Inactive', '1998-03-19'),
(34, 7, 'Kang Hye-won', 'Inactive', '1999-07-05'),
(35, 7, 'Choi Ye-na', 'Inactive', '1999-09-29'),
(36, 7, 'Lee Chae-yeon', 'Inactive', '2000-01-11'),
(37, 7, 'Kim Chae-won', 'Inactive', '2000-08-01'),
(38, 7, 'Kim Min-ju', 'Inactive', '2001-02-05'),
(39, 7, 'Nako Yabuki', 'Inactive', '2001-06-18'),
(40, 7, 'Hitomi Honda', 'Inactive', '2001-10-06'),
(41, 7, 'Jo Yu-ri', 'Inactive', '2001-10-22'),
(42, 7, 'An Yu-jin', 'Inactive', '2003-09-01'),
(43, 7, 'Jang Won-young', 'Inactive', '2004-08-31'),
(44, 8, 'Lee Ji-eun (IU)', 'Active', '1993-05-16'),
(45, 9, 'Mai', 'Active', '2004-11-10'),
(46, 9, 'Bang Jee-min', 'Active', '2005-05-08'),
(47, 9, 'Koko', 'Active', '2006-11-14'),
(48, 9, 'Ryu Sa-rang', 'Active', '2007-06-18'),
(49, 9, 'Choi Jung-eun', 'Active', '2007-02-12'),
(50, 9, 'Jeong Sae-bi', 'Active', '2008-01-22'),
(51, 10, 'S.Coups (Choi Seung-cheol)', 'Active', '1995-08-08'),
(52, 10, 'Jeonghan (Yoon Jeong-han)', 'Inactive', '1995-10-04'),
(53, 10, 'Joshua (Hong Ji-soo)', 'Active', '1995-12-30'),
(54, 10, 'Jun (Wen Junhui)', 'Active', '1996-06-10'),
(55, 10, 'Hoshi (Kwon Soon-young)', 'Active', '1996-06-15'),
(56, 10, 'Wonwoo (Jeon Won-woo)', 'Active', '1996-07-17'),
(57, 10, 'Woozi (Lee Ji-hoon)', 'Inactive', '1996-11-22'),
(58, 10, 'DK (Lee Seok-min)', 'Active', '1997-02-18'),
(59, 10, 'Mingyu (Kim Min-gyu)', 'Active', '1997-04-06'),
(60, 10, 'The8 (Xu Minghao)', 'Active', '1997-11-07'),
(61, 10, 'Seungkwan (Boo Seung-kwan)', 'Active', '1998-01-16'),
(62, 10, 'Vernon (Hansol Vernon Choi)', 'Active', '1998-02-18'),
(63, 10, 'Dino (Lee Chan)', 'Active', '1999-02-11'),
(64, 11, 'Jin Hyeon-ju', 'Active', '2001-11-03'),
(65, 11, 'Nana', 'Active', '2007-06-06'),
(66, 11, 'Gehlee Dangca', 'Active', '2007-08-19'),
(67, 11, 'Kotoko', 'Active', '2007-10-28'),
(68, 11, 'Bang Yun-ha', 'Active', '2009-02-28'),
(69, 11, 'Elisia', 'Active', '2009-04-18'),
(70, 11, 'Oh Yoon-a', 'Active', '2009-10-07'),
(71, 11, 'Lim Seo-won', 'Active', '2011-01-27');

-- 4. REF_NATIONALITY TABLE (Child, references Member)
INSERT INTO REF_Nationality (Nationality_ID, Nationality_Name) VALUES
(1, 'South Korean'),
(2, 'New Zealander'),
(3, 'Thai'),
(4, 'American'),
(5, 'Australian'),
(6, 'Japanese'),
(7, 'Chinese'),
(8, 'Canadian'),
(9, 'Vietnamese'),
(10, 'Filipino');

-- 5. LINK_MEMBER_NATIONALITY TABLE (Junction, references Member and Nationality)
INSERT INTO LINK_Member_Nationality (Member_ID, Nationality_ID) VALUES
(1, 1), (2, 1), (3, 2), (4, 3), (5, 1), (6, 1), (7, 1), (7, 4), (8, 1), (8, 5),
(9, 1), (10, 1), (11, 6), (12, 1), (13, 7), (14, 1), (15, 1), (16, 1), (17, 7),
(18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1), (24, 6), (24, 1), (25, 1),
(26, 7), (27, 1), (28, 9), (28, 5), (29, 1), (29, 5), (30, 1), (31, 1), (32, 1),
(33, 6), (34, 1), (35, 1), (36, 1), (37, 1), (38, 1), (39, 6), (40, 6), (41, 1),
(42, 1), (43, 1), (44, 1), (45, 6), (46, 1), (47, 6), (48, 1), (49, 1), (50, 1),
(51, 1), (52, 1), (53, 4), (53, 1), (54, 7), (55, 1), (56, 1), (57, 1), (58, 1),
(59, 1), (60, 7), (61, 1), (62, 4), (62, 1), (63, 1), (64, 1), (65, 6), (66, 10),
(67, 6), (68, 1), (69, 10), (70, 1), (71, 1);

-- 6. REF_ROLE TABLE () (Child, references Member)
INSERT INTO REF_Role (Role_ID, Role_Name) VALUES
(1, 'Vocalist'),
(2, 'Visual'),
(3, 'Rapper'),
(4, 'Dancer'),
(5, 'Maknae'),
(6, 'Leader'),
(7, 'Producer'),
(8, 'Center'),
(9, 'Singer-Songwriter'),
(10, 'Actress'),
(11, 'General Leader'),
(12, 'Performance Leader'),
(13, 'Vocal Leader'),
(14, 'Main Vocalist'),
(15, 'Lead Vocalist'),
(16, 'Main Rapper'),
(17, 'Lead Rapper'),
(18, 'Main Dancer');

-- 7. LINK_MEMBER_ROLE TABLE (Child, references Member)
INSERT INTO LINK_Member_Role (Member_ID, Role_ID) VALUES
(1, 1), (1, 2), (2, 3), (2, 1), (3, 1), (3, 4), (4, 4), (5, 6), (5, 1), (5, 4),
(6, 1), (6, 4), (7, 3), (7, 4), (7, 1), (8, 3), (8, 1), (9, 1), (9, 4), (9, 2),
(10, 1), (10, 5), (11, 4), (11, 3), (11, 5), (12, 1), (12, 3), (13, 8), (13, 1),
(14, 6), (14, 1), (14, 4), (15, 1), (15, 3), (16, 1), (16, 7), (16, 13), (17, 1),
(17, 3), (18, 1), (18, 3), (19, 3), (19, 4), (19, 1), (20, 1), (20, 4), (20, 5),
(21, 1), (21, 3), (21, 7), (22, 1), (22, 5), (23, 6), (23, 4), (23, 3), (23, 1),
(24, 3), (24, 1), (25, 1), (25, 4), (26, 1), (26, 5), (27, 6), (27, 1), (27, 4),
(28, 1), (28, 4), (29, 1), (29, 4), (30, 1), (30, 4), (31, 1), (31, 4), (31, 5),
(32, 6), (32, 1), (32, 4), (33, 1), (33, 3), (33, 2), (34, 3), (34, 1), (34, 2),
(35, 3), (35, 1), (35, 4), (36, 4), (36, 1), (36, 3), (37, 1), (37, 4), (38, 1),
(38, 3), (38, 2), (39, 1), (40, 4), (40, 1), (41, 1), (42, 1), (42, 4), (43, 8),
(43, 1), (43, 5), (44, 9), (44, 1), (44, 10), (45, 1), (45, 4), (46, 4), (46, 1),
(46, 8), (47, 3), (47, 4), (48, 1), (48, 4), (49, 14), (50, 1), (50, 5), (51, 11),
(51, 16), (52, 15), (53, 15), (54, 4), (54, 1), (55, 12), (55, 18), (56, 17),
(57, 13), (57, 7), (58, 14), (59, 17), (59, 2), (60, 4), (60, 1), (61, 14),
(62, 16), (63, 18), (63, 5), (64, 6), (64, 1), (65, 4), (66, 1), (67, 4), (68, 1),
(69, 1), (69, 4), (70, 1), (71, 1), (71, 5);

-- 8. ARTIST_EVENT TABLE (Junction, references Artist and Event)
-- NOTE: Assuming 'Event' records are already inserted or the table is not required to be inserted first.
INSERT INTO Artist_Event (Artist_ID, Event_ID) VALUES
(1, 1),
(2, 2),
(3, 3),  
(5, 5),
(8, 26), 
(9, 27),
(1, 28),
(10, 29),
(3, 30), 
(3, 31),
(2, 31), 
(5, 31); 

-- 9. ARTIST_FOLLOWER TABLE (Junction, references Artist and Fan)
-- NOTE: Assuming 'Fan' records are already inserted or the table is not required to be inserted first.
INSERT INTO Artist_Follower (Artist_ID, Fan_ID, Followed_Date) VALUES
(5, 1, '2025-11-17'),
(7, 1, '2025-11-17'),
(6, 2, '2025-11-17'),
(1, 3, '2025-11-17'),
(10, 3, '2025-11-17'),
(2, 4, '2025-11-17'),
(1, 5, '2025-11-17'),
(5, 6, '2025-11-17'),
(10, 7, '2025-11-17'),
(11, 8, '2025-11-17');

-- 10. SONG TABLE 
INSERT INTO Song (Song_Name) VALUES
('Pink Venom'), 
('How You Like That'), 
('Shut Down'), 
('DDU-DU DDU-DU'), 
('Kill This Love'), 
('As If It''s Your Last'), 
('Drunk-Dazed'), 
('Sweet Venom'), 
('Polaroid Love'), 
('Bite Me'), 
('In Bloom'), 
('CRUSH'), 
('Black Mamba'), 
('Next Level'), 
('Savage'), 
('Drama'), 
('Supernova');

-- 10. SETLIST TABLE (Junction, references Artist and Event)
INSERT INTO Setlist (Artist_ID, Event_ID, Song_ID, Play_Order) VALUES
-- BLACKPINK Comeback Tour 
(1, 1, 1, 1),
(1, 1, 2, 2),
(1, 1, 3, 3),
(1, 1, 4, 4),
(1, 1, 5, 5),
(1, 1, 6, 6),
-- ENHYPEN Dunkin Donut Collab x Fanmeet 
(2, 2, 7, 1),
(2, 2, 8, 2),
(2, 2, 9, 3),
(2, 2, 10, 4),
-- ZB1 Hi-Five Session
(3, 3, 11, 1),
(3, 3, 12, 2),
-- AESPA Artist Showcase 
(5, 5, 13, 1),
(5, 5, 14, 2),
(5, 5, 15, 3),
(5, 5, 16, 4),
(5, 5, 17, 5);

INSERT INTO Fanclub (Fanclub_ID, Fanclub_Name, Artist_ID) 
VALUES  (1, 'Zero Days', 3),
        (2, 'WinRina 4ever', 5),
        (3, 'AKKADEMY', 4),
        (4, 'BLINKS United', 1),
        (5, 'ENGENE-ers', 2),
        (6, 'Zerose Squad', 3),
        (7, 'MY Dreams', 5),
        (8, 'Bunnies Forever', 6),
        (9, 'WIZ*ONE Family', 7),
        (10, 'Pink Venom Club', 1),
        (11, 'ENGENE Nation', 2),
        (12, 'NewJeans Denim', 6),
        (13, 'AKMU Lovers', 4),
        (14, 'Aespa Synk', 5),
        (15, 'BP World', 1),
        (16, 'ZB1 Forever', 3),
        (17, 'Tokki Squad', 6),
        (18, 'IZ*ONE Legacy', 7),
        (19, 'ENHYPEN Global', 2),
        (20, 'Suhyun & Chanhyuk Fans', 4),
        (21, 'BLINK Paradise', 1),
        (22, 'Vampire Lovers', 2),
        (23, 'ZB1 United', 3),
        (24, 'AKMU Galaxy', 4),
        (25, 'Next Level Fans', 5),
        (26, 'Bunny Camp', 6),
        (27, 'WIZONE Forever', 7),
        (28, 'Born Pink Squad', 1),
        (29, 'Dimension Lovers', 2),
        (30, 'Zerose International', 3);

INSERT INTO Fanclub_Event (Fanclub_ID, Event_ID) 
VALUES  (3, 4),
        (4, 6),
        (6, 7),
        (5, 9),
        (2, 8),
        (10, 10),
        (7, 11),
        (17, 12),
        (3, 13),
        (8, 14),
        (11, 15),
        (1, 16),
        (15, 17),
        (25, 18),
        (27, 19),
        (26, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (14, 24),
        (20, 25);

INSERT INTO Fanclub_Membership (Fan_ID, Fanclub_ID, Date_Joined) 
VALUES  (5, 2, '2020-10-09'),
        (4, 3, '2008-06-07'),
        (3, 1, '2014-12-13'),
        (2, 5, '2025-01-25'),
        (1, 4, '2021-01-01'),
        (6, 15, '2021-03-25'),
        (17, 23, '2023-09-26'),
        (7, 14, '2022-08-30'),
        (8, 3, '2024-02-19'),
        (5, 5, '2025-07-04'),
        (9, 26, '2023-02-17'),
        (10, 4, '2025-03-15'),
        (11, 29, '2020-10-28'),
        (12, 16, '2024-05-24'),
        (13, 30, '2025-05-02'),
        (14, 27, '2023-08-06'),
        (15, 2, '2022-01-10'),
        (16, 21, '2020-01-26'),
        (17, 13, '2024-07-20'),
        (18, 12, '2024-02-19'),
        (19, 10, '2025-08-17'),
        (20, 11, '2019-10-11'),
        (21, 19, '2023-01-15'),
        (22, 1, '2023-04-02'),
        (23, 25, '2018-06-26'),
        (23, 9, '2018-05-26'),
        (24, 18, '2025-02-24'),
        (25, 8, '2022-06-18'),
        (22, 22, '2022-04-02'),
        (2, 2, '2025-01-24');

use dbapp;
INSERT INTO Merchandise (
    Merchandise_ID, 
    Merchandise_Name,
    Artist_ID,
    Fanclub_ID,
    Merchandise_Description,
    Merchandise_Price, 
    Initial_Stock,
    Quantity_Stock
) VALUES
-- Original Merchandise (IDs 1-76)
(1, 'BLACKPINK World Tour Tee Black', 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a black heavyweight unisex tee.', 4000, 500, 500),
(2, 'BLACKPINK World Tour Tee White', 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a white heavyweight unisex tee.', 4000, 500, 500),
(3, 'BLACKPINK Sticker Set', 1, NULL, 'Includes 1 BLACKPINK logo sticker, 1 Deadline Tour logo sticker, 1 Heart logo sticker, 1 Black heart sticker with BLACKPINK in the middle, 1 Character sticker', 800, 600, 600),
(4, 'BLACKPINK Foil Zip Hoodie White', 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a white unisex zip hoodie.', 7900, 300, 300),
(5, 'BLACKPINK Cuff Beanie Black', 1, NULL, 'Black cuff beanie with BLACKPINK embroidered on the front in pink thread.', 2800, 300, 300),
(6, 'BLACKPINK Official Light Stick Special Edition', 1, NULL, 'The BLACKPINK Official Light Stick Special Edition is an upgraded, premium version of the group’s signature hammer light stick, featuring improved design and enhanced functionality.', 2000, 1000, 998),
(7, 'BLACKPINK Airpods Silicone Case Set', 1, NULL, 'The BLACKPINK AirPods Silicone Case Set is a stylish, protective accessory featuring the group’s signature design for a sleek and durable AirPods cover.', 850, 1000, 1000),
(8, 'ENHYPEN X Dunkin'' Tumbler', 2, NULL, '450 ML tumbler with ENHYPEN x Dunkin’ design', 750, 500, 500),
(9, 'ENHYPEN X Dunkin'' Tote Bag', 2, NULL, 'Eco tote bag featuring Dunkin’ logo and members', 450, 500, 500),
(10, 'ENHYPEN X Dunkin'' Tin Case', 2, NULL, 'Metal tin case for storing photocard sets', 250, 500, 500),
(11, 'ENHYPEN X Dunkin'' Collector''s Set', 2, NULL, 'Complete set with photocard, tote, and tumbler', 1000, 600, 600),
(12, 'ZB1 Hi-Five Polaroid Set', 3, NULL, 'Instant film set with members’ printed signatures', 600, 400, 400),
(13, 'ZB1 Keyring', 3, NULL, 'Official ZB1 acrylic keyring with nameplate', 1000, 700, 700),
(14, 'AKMU Birthday Mug', NULL, 3, 'Ceramic mug celebrating AKMU’s birthday cafe event', 500, 500, 500),
(15, 'AKMU Cupsleeve Set', NULL, 24, 'Collectible cupsleeves from AKMU’s cafe event', 950, 600, 600),
(16, 'AESPA Mini Poster', 5, NULL, 'Limited edition A4 poster from showcase', 800, 700, 700),
(17, 'AESPA Karina Photocard Set', 5, NULL, 'Karina exclusive photocard pack', 850, 800, 800),
(18, 'AESPA Winter Photocard Set', 5, NULL, 'Winter exclusive photocard pack', 850, 800, 797),
(19, 'AESPA Giselle Photocard Set', 5, NULL, 'Giselle exclusive photocard pack', 850, 800, 800),
(20, 'AESPA Ningning Photocard Set', 5, NULL, 'Ningning exclusive photocard pack', 850, 800, 800),
(21, 'Rosé Birthday Cupsleeve Set', NULL, 4, 'Includes collectible cupsleeve, postcard, and sticker set for Rosé’s birthday event.', 500, 400, 400),
(22, 'Rosé Birthday Photocard', NULL, 4, 'Limited edition Rosé birthday photocard.', 150, 600, 600),
(23, 'ZB1 Anniversary Cupsleeve Set', NULL, 6, 'Includes collectible cupsleeve, holographic photocard, and pin badge for ZB1 anniversary.', 600, 500, 500),
(24, 'ZB1 Group Sticker Sheet', NULL, 6, 'Vinyl sticker sheet with ZB1 members and logo for the anniversary.', 250, 700, 700),
(25, 'WinRina Winter Cupsleeve Set', NULL, 2, 'Includes collectible cupsleeve, A5 art print, and keychain for the WinRina winter event.', 750, 450, 450),
(26, 'WinRina Photostrip', NULL, 2, 'Set of two themed photostrips featuring Karina and Winter.', 200, 600, 600),
(27, 'Sunghoon Birthday Cupsleeve Kit', NULL, 5, 'Includes collectible cupsleeve, mini banner, and customized fan.', 550, 400, 400),
(28, 'Sunghoon Acrylic Standee', NULL, 5, 'Sunghoon birthday themed acrylic standee.', 850, 300, 300),
(29, 'Jisoo Birthday Cupsleeve Package', NULL, 10, 'Includes collectible cupsleeve, glitter photocard, and button pin for Jisoo’s birthday.', 500, 500, 500),
(30, 'Jisoo Pop Socket', NULL, 10, 'Custom Jisoo birthday themed pop socket.', 300, 500, 500),
(31, 'Karina Birthday Cupsleeve Set', NULL, 7, 'Includes collectible cupsleeve, exclusive birthday bookmark, and wristband.', 450, 400, 400),
(32, 'Karina Birthday Lanyard', NULL, 7, 'Themed lanyard with Karina’s birthday design.', 350, 500, 500),
(33, 'Hanni Cupsleeve Set', NULL, 17, 'Includes collectible cupsleeve, lenticular card, and themed decal sticker.', 550, 450, 450),
(34, 'Hanni Mini Washi Tape', NULL, 17, 'Mini roll of decorative washi tape featuring Hanni.', 200, 600, 600),
(35, 'Chanhyuk Birthday Cupsleeve Set', NULL, 3, 'Includes collectible cupsleeve, special photocard, and Chanhyuk-themed doodle magnet.', 500, 350, 350),
(36, 'AKMU Lyrics Postcard Set', NULL, 3, 'Set of 4 postcards featuring AKMU song lyrics.', 400, 400, 400),
(37, 'Hyein Cupsleeve Kit', NULL, 8, 'Includes collectible cupsleeve, polaroid print set, and keyring charm.', 600, 400, 400),
(38, 'Hyein Hair Clip Set', NULL, 8, 'Set of two themed hair clips.', 350, 500, 500),
(39, 'Jungwon Birthday Cupsleeve Set', NULL, 11, 'Includes collectible cupsleeve, birthday postcard, and holographic sticker.', 450, 500, 500),
(40, 'Jungwon Fabric Poster', NULL, 11, 'Small fabric poster with Jungwon’s birthday design.', 600, 300, 300),
(41, 'Hanbin Birthday Cupsleeve Package', NULL, 1, 'Includes collectible cupsleeve, lenticular photocard, and special member badge.', 550, 450, 450),
(42, 'Hanbin Photo Film Strip', NULL, 1, 'Set of two Hanbin-themed photo film strips.', 200, 600, 600),
(43, 'Lisa Birthday Cupsleeve Set', NULL, 15, 'Includes collectible cupsleeve, exclusive sticker pack, and photostrip.', 500, 400, 398),
(44, 'Lisa Pin Badge', NULL, 15, 'Custom design Lisa birthday pin badge.', 250, 500, 500),
(45, 'Winter Cupsleeve Set', NULL, 25, 'Includes collectible cupsleeve, special keyring, and mini-fan.', 600, 350, 350),
(46, 'Winter Photocard Set (Fanmade)', NULL, 25, 'Set of 5 fanmade photocards of Winter.', 400, 400, 400),
(47, 'Sakura Cupsleeve Package', NULL, 27, 'Includes collectible cupsleeve, mini-poster, and reflective sticker.', 500, 400, 400),
(48, 'Sakura ID Photocard', NULL, 27, 'Sakura ID style photocard.', 150, 600, 600),
(49, 'Minji Birthday Cupsleeve Kit', NULL, 26, 'Includes collectible cupsleeve, 4-cut photostrip, and custom bookmark.', 500, 450, 450),
(50, 'Minji Rabbit Plushie Keychain', NULL, 26, 'Small plushie keychain with a rabbit design.', 700, 300, 300),
(51, 'Jennie Birthday Cupsleeve Set', NULL, 21, 'Includes collectible cupsleeve, quote postcard, and themed sticker sheet.', 500, 500, 500),
(52, 'Jennie Mini Polaroid Set', NULL, 21, 'Set of 3 mini polaroid prints of Jennie.', 250, 500, 500),
(53, 'Heeseung Cupsleeve Set', NULL, 22, 'Includes collectible cupsleeve, exclusive photocard, and themed art print.', 550, 400, 400),
(54, 'Heeseung Fanmade Bracelet', NULL, 22, 'Beaded bracelet with Heeseung’s name/initials.', 300, 350, 350),
(55, 'Jiwoong Birthday Cupsleeve Package', NULL, 23, 'Includes collectible cupsleeve, birthday slogan, and photocard.', 500, 450, 450),
(56, 'Jiwoong Photo Binder', NULL, 23, 'Small A5 photo binder for photocards.', 800, 300, 300),
(57, 'Ningning Cupsleeve Set', NULL, 14, 'Includes collectible cupsleeve, postcard set, and holographic sticker.', 450, 400, 400),
(58, 'Ningning Pop-up Photocard', NULL, 14, '3D Pop-up photocard of Ningning.', 200, 500, 500),
(59, 'AKMU Anniversary Cupsleeve Duo Set', NULL, 20, 'Includes two collectible cupsleeves (Suhyun and Chanhyuk), and a special anniversary photocard.', 700, 400, 400),
(60, 'AKMU Logo Tote Bag (Fanmade)', NULL, 20, 'Small fanmade tote bag with AKMU logo and anniversary text.', 550, 300, 300),
(61, 'IU Blooming in Blue Concert Tee', 8, NULL, 'Official concert t-shirt in blue, with tour name and dates.', 3500, 800, 798),
(62, 'IU Official Light Stick Ver. 3', 8, NULL, 'IU’s official light stick, the third version.', 2500, 1500, 1500),
(63, 'IU Photo Slogan', 8, NULL, 'Large fabric slogan with IU’s photo and name.', 900, 1000, 1000),
(64, 'IZNA Anniversary Slogan Towel', 9, NULL, 'Small commemorative hand towel with IZNA anniversary logo.', 700, 500, 500),
(65, 'IZNA Unit Photocard Set', 9, NULL, 'Set of unit photocards from the anniversary fanmeet.', 800, 600, 600),
(66, 'LISA Lovesick Tour Hoodie', 1, NULL, 'Official black hoodie with LISA Lovesick Tour logo.', 7500, 400, 398),
(67, 'LISA Photo Card Binder', 1, NULL, 'Small photo card collector binder, black and gold themed.', 1500, 500, 500),
(68, 'LISA Lovesick Official Light Stick Topper', 1, NULL, 'Interchangeable topper for the BLACKPINK light stick with a LISA design.', 1000, 700, 700),
(69, 'SEVENTEEN Tour T-Shirt', 10, NULL, 'Official tour t-shirt with comeback theme.', 4000, 800, 800),
(70, 'SEVENTEEN Cheering Kit', 10, NULL, 'Includes slogan, banner, and cheering accessories.', 1200, 1000, 997),
(71, 'SEVENTEEN Official Light Stick Ver. 4', 10, NULL, 'SEVENTEEN’s official light stick, the fourth version.', 2500, 1500, 1500),
(72, 'ZB1 Summer Concert Tee', 3, NULL, 'Light blue t-shirt with ZB1 Summer in Manila event logo.', 3800, 700, 700),
(73, 'ZB1 Photo Film Set (Concert Ver.)', 3, NULL, 'Set of 5 film-style photocards from the concert.', 500, 800, 800),
(74, 'ZB1 Summer Concert Fan', 3, NULL, 'Handheld electric fan with ZB1 logo.', 900, 600, 596),
(75, 'UNIS Asia Stage Official Hoodie', 11, NULL, 'Black official hoodie from the Asia Stage event.', 4500, 500, 500),
(76, 'UNIS Light Stick Charm Set', 11, NULL, 'Set of charms to decorate the official light stick.', 850, 700, 700),
(77, 'BLACKPINK Vinyl Record (The Album)', 1, NULL, 'Limited edition pink vinyl record of BLACKPINK’s first studio album.', 4500, 700, 700),
(78, 'BLINK Official Membership Kit', 1, NULL, 'The annual BLINK membership kit including a photobook, badge set, and member cards.', 3500, 1000, 999),
(79, 'ENHYPEN Logo Keychain', 2, NULL, 'Official acrylic keyring with ENHYPEN’s group logo.', 900, 800, 798),
(80, 'ENGENE Official Fan Kit 2026', 2, NULL, 'The official ENGENE annual fan kit with exclusive merchandise, photocard sets, and fanbook.', 4000, 1000, 1000),
(81, 'ENHYPEN World Tour Photo Essay', 2, NULL, 'Official photo essay book capturing behind-the-scenes moments from their recent world tour.', 2500, 600, 600),
(82, 'ZB1 Debut Mini Photobook', 3, NULL, 'Mini photobook commemorating the group’s debut.', 1800, 800, 800),
(83, 'ZEROSE Official Membership Card', 3, NULL, 'Official physical membership card for the ZEROSE fanclub.', 1000, 2000, 1997),
(84, 'ZB1 Group Slogan Towel', 3, NULL, 'High-quality fabric slogan towel featuring all nine members.', 1100, 900, 900),
(85, 'AKMU Re-Imagined Album LP', 4, NULL, 'Vinyl LP record of AKMU’s re-imagined greatest hits album.', 5000, 500, 500),
(86, 'AKMU "Sailing" Poster Set', 4, NULL, 'Set of 4 official posters from the "Sailing" era.', 1200, 700, 700),
(87, 'AKMU Official Slogan Towel', 4, NULL, 'Official fabric slogan towel with AKMU’s logo and name.', 800, 900, 895),
(88, 'MY Official Membership Kit', 5, NULL, 'The annual MY membership kit including exclusive ID card, pin set, and stationary.', 3800, 1100, 1096),
(89, 'AESPA Logo Patch Set', 5, NULL, 'Set of embroidered patches featuring the AESPA and member logos.', 750, 900, 900),
(90, 'AESPA Synk Hyperline Blu-ray', 5, NULL, 'Concert Blu-ray disc of the Synk: Hyper Line world tour.', 4500, 500, 500),
(91, 'Bunnies Official Membership Kit', 6, NULL, 'The annual Bunnies membership kit featuring exclusive photo cards and a tin case.', 3600, 1000, 1000),
(92, 'NewJeans 1st EP Bluebook Ver.', 6, NULL, 'The physical album release of NewJeans 1st EP (Bluebook Version).', 1500, 1500, 1497),
(93, 'NewJeans Bunny Keyring', 6, NULL, 'Small metal keyring in the shape of the group’s signature rabbit logo.', 800, 1200, 1200),
(94, 'UAENA Official Fan Kit 2026', 8, NULL, 'The annual UAENA official fan kit with photocards, photobook, and fan-exclusive items.', 4200, 800, 800),
(95, 'IU Photo Slogan Set', 8, 7, 'Set of three high-quality fabric slogans featuring different IU photos.', 1500, 700, 699),
(96, 'IU Concert Merch T-Shirt (Generic)', 8, NULL, 'Simple, high-quality t-shirt with IU’s stylized name on the chest.', 2800, 600, 600),
(97, 'CARAT Official Membership Kit', 10, NULL, 'The annual CARAT membership kit with exclusive keyring, photobook, and badge.', 3900, 1000, 1000),
(98, 'SEVENTEEN Logo Hat', 10, NULL, 'Official baseball cap with the SEVENTEEN logo embroidered on the front.', 2500, 600, 600),
(99, 'SEVENTEEN 13 Member Photocard Pack', 10, NULL, 'Official photocard pack containing one card for each of the thirteen members.', 950, 1100, 1096),
(100, 'IZNA Official Membership Kit', 9, NULL, 'The official IZNA membership kit, including a personalized card and exclusive merch.', 3700, 900, 900),
(101, 'IZNA Group Photocard Pack', 9, NULL, 'Official photocard pack featuring all members of IZNA.', 650, 1200, 1200),
(102, 'IZNA Official Fan Towel', 9, NULL, 'Standard sized fan towel with the IZNA logo.', 900, 700, 700),
(103, 'ENHYPEN Official Light Stick Ver. 2', 2, NULL, 'The official ENHYPEN light stick (Engene Bong) version 2, featuring a compass design and improved connectivity.', 2400, 800, 797),
(104, 'ZB1 Official Light Stick Ver. 1 (ZB Bong)', 3, NULL, 'The official light stick for ZEROBASEONE, featuring a star design and ZEROSE heart logo.', 2500, 900, 896),
(105, 'AKMU Sailing Official Light Stick', 4, NULL, 'A unique light stick designed to resemble a small, stylized sail/flag from the Sailing era.', 2200, 450, 445),
(106, 'AESPA Official Light Stick Ver. 1', 5, NULL, 'The official AESPA light stick, shaped like the logo with a minimalist design.', 2300, 850, 846),
(107, 'NewJeans Binky Bong Light Stick', 6, NULL, 'The official NewJeans light stick, featuring the iconic bunny shape.', 2500, 950, 945),
(108, 'IZNA Official Light Stick', 9, NULL, 'The official IZNA light stick, designed with a sleek, futuristic aesthetic.', 2100, 750, 750),
(109, 'UNIS Official Light Stick', 11, NULL, 'The official UNIS light stick, featuring a design representing unity and stars.', 2300, 700, 700);

INSERT INTO Merchandise_Event (Merchandise_ID, Event_ID) VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7,1), -- BLACKPINK Comeback Tour (Event 1)
(8, 2), (9, 2), (10, 2), (11, 2),       -- ENHYPEN Dunkin Donut Collab (Event 2)
(12, 3), (13, 3),                       -- ZB1 Hi-Five Session (Event 3)
(14, 4), (15, 4),            -- AKMU Birthday Cupsleeve Cafe (Event 4) (Note: Merch 22 was also linked here)
(16, 5), (17, 5), (18, 5), (19, 5), (20, 5), -- AESPA Artist Showcase (Event 5)
(21, 6), (22,6),                                -- BLINKS United Rosé Birthday Event (Event 6)
(23, 7), (24, 7),                       -- Zerose Squad Anniversary Exhibit (Event 7)
(25, 8), (26, 8),                       -- WinRina 4ever Winter Cupsleeve Cafe (Event 8)
(27, 9), (28, 9),                       -- ENGENE-ers Sunghoon Birthday Cupsleeve (Event 9)
(29, 10), (30, 10),                     -- Pink Venom Club Jisoo Cupsleeve (Event 10)
(31, 11), (32, 11),                     -- MY Dreams Karina Birthday Cupsleeve (Event 11)
(33, 12), (34, 12),                     -- Tokki Squad Hanni Cupsleeve Event (Event 12)
(35, 13), (36, 13),                     -- AKKADEMY Chanhyuk Birthday Cupsleeve (Event 13)
(37, 14), (38, 14),                     -- Bunnies Forever Hyein Cupsleeve (Event 14)
(39, 15), (40, 15),                     -- ENGENE Nation Jungwon Cupsleeve (Event 15)
(41, 16), (42, 16),                     -- Zero Days Hanbin Birthday Cupsleeve (Event 16)
(43, 17), (44, 17),                     -- BP World Lisa Birthday Cupsleeve (Event 17)
(45, 18), (46, 18),                     -- Next Level Fans Winter Cupsleeve (Event 18)
(47, 19), (48, 19),                     -- WIZONE Forever Sakura Photozone (Event 19)
(49, 20), (50, 20),                     -- Bunny Camp Minji Birthday Exhbit (Event 20)
(51, 21), (52, 21),                     -- BLINK Paradise Jennie Cupsleeve (Event 21)
(53, 22), (54, 22),                     -- Vampire Lovers Heeseung Cupsleeve (Event 22)
(55, 23), (56, 23),                     -- ZB1 United Jiwoong Birthday Cupsleeve (Event 23)
(57, 24), (58, 24),                     -- Aespa Synk Ningning Cupsleeve (Event 24)
(59, 25), (60, 25),                     -- Suhyun & Chanhyuk Fans Anniversary Cupsleeve (Event 25)
(61, 26), (62, 26), (63, 26),           -- IU Concert: Blooming in Blue (Event 26)
(64, 27), (65, 27),                     -- IZNA Anniversary Fanmeet (Event 27)
(66, 28), (67, 28), (68, 28),           -- LISA: Lovesick Concert (Event 28)
(69, 29), (70, 29), (71, 29),           -- SEVENTEEN Comeback Tour (Event 29)
(72, 30), (73, 30), (74, 30),           -- ZB1 Summer in Manila Concert (Event 30)
(75, 31), (76, 31), (6, 31), (103, 31), (104, 31), (105, 31), (106, 31), (107, 31), (108, 31), (109, 31), (71, 31);  -- KPOP Con: Manila Stage (Event 31)



INSERT INTO `Order` (Order_ID, Fan_ID, Order_Date, Order_Status) VALUES
(1, 1, '2025-09-02 10:00:00', 'Paid'),      
(2, 2, '2025-09-02 12:30:00', 'Paid'),   
(3, 3, '2025-09-03 09:15:00', 'Paid'),      
(4, 4, '2025-09-03 15:45:00', 'Paid'), 
(5, 5, '2026-09-04 11:20:00', 'Paid'),      
(6, 6, '2026-09-04 16:50:00', 'Paid'),   
(7, 7, '2026-09-05 08:00:00', 'Paid'),      
(8, 8, '2026-09-05 13:10:00', 'Paid'),      
(9, 9, '2026-09-06 10:40:00', 'Paid'), 
(10, 10, '2026-09-06 17:55:00', 'Paid'),     
(11, 11, '2026-09-07 11:30:00', 'Paid'),  
(12, 12, '2026-09-07 14:00:00', 'Paid'),     
(13, 13, '2026-09-08 09:25:00', 'Paid'),     
(14, 14, '2026-09-08 18:05:00', 'Paid'),     
(15, 15, '2026-09-09 10:15:00', 'Paid'),
(16, 16, '2026-09-09 13:50:00', 'Paid'),     
(17, 17, '2027-09-10 11:10:00', 'Paid'),  
(18, 18, '2027-09-10 15:20:00', 'Paid'),     
(19, 19, '2027-09-11 09:40:00', 'Paid'),     
(20, 20, '2027-09-11 16:15:00', 'Paid');     


-- ==========================================================
-- 3. INSERT DATA INTO THE `Purchase_List` TABLE (20 Records)
-- Order_IDs are now 1 through 20
-- ==========================================================

INSERT INTO `Purchase_List` (Order_ID, Merchandise_ID, Quantity_Purchased) VALUES
(1, 6, 2),   
(2, 103, 3),  
(3, 104, 4),  
(4, 87, 5),   
(5, 106, 4),  
(6, 92, 3),   
(7, 61, 2),   
(8, 95, 1),   
(9, 79, 2),   
(10, 70, 3),  
(11, 74, 4),  
(12, 105, 5), 
(13, 88, 4),  
(14, 83, 3),  
(15, 66, 2),  
(16, 78, 1),  
(17, 43, 2),  
(18, 18, 3),  
(19, 99, 4),  
(20, 107, 5);