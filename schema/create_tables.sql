-- ==========================================================
--  This SQL Script is ONLY FOR CREATING TABLES.
--  Add foreign keys on 'constraints.sql'
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `dbApp`;
USE dbApp;

-- ===============================================
--                  CORE TABLES
-- ===============================================

--
-- Table structure for table `users`
--
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `date_joined` DATE NOT NULL,  -- is this really needed
    
    PRIMARY KEY (`id`),

    -- Ensures non-duplication of username/email
    UNIQUE (`username`),
    UNIQUE (`email`)
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
	`Manager_ID` INT(11) NOT NULL,
    `Artist_Name` VARCHAR(255) NOT NULL,
	`Nationality` VARCHAR(255),
	`Activity_Status` ENUM('Active', 'Inactive', 'Hiatus') NOT NULL,
    `Debut_Date` DATE NOT NULL,
    `Debut_Days` INT NOT NULL,
    PRIMARY KEY (`Artist_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- 
-- Table structure for `merchandise`
--
DROP TABLE IF EXISTS `merchandise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchandise` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `artist_id` INT NOT NULL,
    `event_id` INT(11) NOT NULL,
    `fanclub_id` INT,
    `price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `quantity_stock` INT NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE (`event_id`, `name`),
    CHECK (`price` >= 0),
    CHECK (`quantity_stock` >= 0)

    -- FOREIGN KEY (`artist_id`) REFERENCES artists(`id`)
    --     ON UPDATE CASCADE,
    -- FOREIGN KEY (`event_id`) REFERENCES events(`id`)
    --     ON DELETE CASCADE
    --     ON UPDATE CASCADE,
    -- FOREIGN KEY (`fanclub_id`) REFERENCES fanclubs(`id`)
    --     ON UPDATE CASCADE,

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
    `Event_Type` SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve') NOT NULL,
	`Date` DATETIME NOT NULL,
    `Venue_ID` INT NOT NULL,
	
    PRIMARY KEY (`Event_ID`),
    -- FOREIGN KEY (`artist_id`) REFERENCES artists(`id`),
    -- FOREIGN KEY (`fanclub_id`) REFERENCES fanclubs(`id`),
    -- FOREIGN KEY (`venue_id`) REFERENCES venues(`id`),
    UNIQUE (`Venue_ID`, `Date`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


-- ================================================
--               ADDITIONAL TABLES
-- ================================================

--
-- Table structure for `fanclubs`
--
DROP TABLE IF EXISTS `fanclubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fanclubs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `fanclub_name` VARCHAR(50) NOT NULL,
    `artist_id` INT NOT NULL,
    `num_members` INT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`id`),
    UNIQUE (`fanclub_name`, `artist_id`)     -- Ensures that no two fanclubs of the same artist share a name
    -- FOREIGN KEY (`artist_id`) REFERENCES artists(`id`),

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
    `Location` VARCHAR(255) NOT NULL, 
    `Capacity` INT NOT NULL CHECK (capacity > 0),
    
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
    UNIQUE (`Section_Name`, `Venue_ID`) -- Prevents duplicate venues with the same name and location
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Seat`
--
DROP TABLE IF EXISTS `Seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seats` (
	`Seat_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Venue_ID` INT(11) NOT NULL,
    `Section_ID` INT(11) NOT NULL,
    `Row_Number` INT NOT NULL, 
    `Seat_Number` INT NOT NULL,
    
    PRIMARY KEY (`Seat_ID`),
	UNIQUE (`Venue_ID`, `Section_ID`, `Row_Number`, `Seat_Number`) -- Prevents duplicates of the seat

    -- FOREIGN KEY (`venue_id`) REFERENCES venues(`venue_id`)
	-- 	ON DELETE CASCADE ON UPDATE CASCADE,
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
    `Event_ID` INT NOT NULL,
    `Tier_Name` VARCHAR(100) NOT NULL DEFAULT 'General Admissions',
    `Price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `Total_Quantity` INT NOT NULL DEFAULT 0,
	`Benefits` VARCHAR(150),
	
	PRIMARY KEY (`Tier_ID`),
    UNIQUE (`Event_ID`, `Tier_Name`)
    -- FOREIGN KEY (`Event_ID`) REFERENCES events(`Event_ID`),
    -- -- Ensures that there is enough slots available
    -- CONSTRAINT check_qty CHECK (`quantity_sold` <= `total_quantity`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manager` (
	`Manager_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Manager_Name` VARCHAR(255) NOT NULL,
	`Contact_Num` VARCHAR(11),
    `Contact_Email` VARCHAR(255),
    `Agency_Address` VARCHAR(255),
    PRIMARY KEY (`Manager_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Member_Detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Member_Detail` (
	`Member_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Artist_ID` INT(11) NOT NULL,
    `Member_Name` VARCHAR(255) NOT NULL,
    `Role` VARCHAR(255),
    `Activity_Status` ENUM('Active', 'Inactive', 'Hiatus') NOT NULL,
    `Birth_Date` DATE, 
    `Age` INT(2),
    PRIMARY KEY (`Member_ID`),
    UNIQUE KEY `uk_artist_member_id` (`Artist_ID`, `Member_ID`)
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

-- ==============================================
--              TRANSACTION TABLES
-- ==============================================

-- 
-- Table structure for `merchandise sales`
--
DROP TABLE IF EXISTS `merchandise_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchandise_sales` (
   `order_number` INT NOT NULL AUTO_INCREMENT,
   `merchandise_id` INT NOT NULL,
   `user_id` INT NOT NULL,

    PRIMARY KEY (order_number)
    -- FOREIGN KEY (merchandise_id) REFERENCES merchandise(id),
    -- FOREIGN KEY (user_id) REFERENCES users(id)
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
    `User_ID` INT NOT NULL,
    `Event_ID` INT NOT NULL,
    `Tier_ID` INT NOT NULL,
    `Seat_ID` INT,
    `Purchase_Date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`Ticket_ID`)
    -- FOREIGN KEY (`user_id`) REFERENCES Users(`Ticket_ID`),
    -- FOREIGN KEY (`event_id`) REFERENCES Events(`Event_ID`),
    -- FOREIGN KEY (`tier_id`) REFERENCES Ticket_Tier(`Tier_ID`),
    -- FOREIGN KEY (`seat_id`) REFERENCES Seats(`Seat_ID`),

    -- -- Ensures that only one seat per event and tier is sold
    -- -- (works for free seating where seat is NULL)
    -- CONSTRAINT is_ticket_unique UNIQUE (event_id, tier_id, seat_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fanclub_membership`
--
DROP TABLE IF EXISTS `fanclub_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fanclub_membership` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `fanclub_id` INT NOT NULL,
    `date_joined` DATE NOT NULL,
    
    PRIMARY KEY (`id`),
    UNIQUE (`user_id`, `fanclub_id`) -- Ensures that a user does not join a fanclub twice

    -- -- Removes membership records upon user deletion
    -- FOREIGN KEY (`user_id`) REFERENCES users(`id`) ON DELETE CASCADE,
    -- -- Removes membership records upon fanclub deletion
    -- FOREIGN KEY (`fanclub_id`) REFERENCES fanclubs(`id`) ON DELETE CASCADE,
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;




