-- ==========================================================
--  This SQL Script is ONLY FOR CREATING TABLES.
--  Add foreign keys on 'constraints.sql'
-- ==========================================================

DROP DATABASE dbApp;
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
    `Days_Since` INT(11) NOT NULL,
    
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
-- Table structure for `Merchandise`
--
DROP TABLE IF EXISTS `Merchandise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Merchandise` (
    `ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(100) NOT NULL,
    `Artist_ID` INT(11) NOT NULL,
    `Event_ID` INT(11),
    `Fanclub_ID` INT(11),
    `Description` VARCHAR(500) DEFAULT NULL,
    `Price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `Initial_Stock` INT(6) NOT NULL DEFAULT 0,
    `Quantity_Stock` INT(6) NOT NULL DEFAULT 0,

    PRIMARY KEY (`ID`),
    UNIQUE (`Event_ID`, `Name`),

	CHECK (`Price` >= 0),
    CHECK (`Initial_Stock` >= 0),
    CHECK (`Quantity_Stock` >= 0)
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
    `Venue_ID` INT(11) NOT NULL,
	`Start_Date` DATE NOT NULL,
	`End_Date` DATE NOT NULL,
	`Start_Time` TIME NOT NULL,
	`End_Time` TIME,
	
    PRIMARY KEY (`Event_ID`),
	CONSTRAINT is_valid_datetime CHECK(
		(`End_Date` > `Start_Date`) OR
		(`End_Date` = `Start_Date` AND `End_Time` > `Start_Time`)
	)
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
    `Artist_ID` INT NOT NULL,
    
    PRIMARY KEY (`Fanclub_ID`),
    UNIQUE (`Fanclub_Name`, `Artist_ID`)     -- Ensures that no two fanclubs of the same artist share a name
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
    `Tier_Name` VARCHAR(100) NOT NULL DEFAULT 'General Admissions',
    `Price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `Total_Quantity` INT NOT NULL DEFAULT 0,
	`Benefits` VARCHAR(150),
	
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
    `City` VARCHAR(255),
	`Country` VARCHAR(255) NOT NULL,
    `Capacity` INT NOT NULL CHECK (capacity > 0),
    
    PRIMARY KEY (`Venue_ID`),
    UNIQUE (`Venue_Name`, `Country`, `City`) -- Prevents duplicate venues with the same name and location
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
    `Seat_Row` VARCHAR(2) NOT NULL, 
    `Seat_Number` INT NOT NULL,
    
    PRIMARY KEY (`Seat_ID`),
	UNIQUE (`Venue_ID`, `Section_ID`, `Seat_Row`, `Seat_Number`) -- Prevents duplicates of the seat
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
-- Table structure for `order`
--
DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order` (
    `Order_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Fan_ID` INT(11) NOT NULL,
    `Order_Date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Status` ENUM('Pending', 'Paid', 'Cancelled', 'Refunded') NOT NULL DEFAULT 'Pending',

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
    `Quantity` INT(5) NOT NULL DEFAULT 1,

    PRIMARY KEY (`Purchase_List_ID`),
	CHECK (`quantity` > 0)
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
    CONSTRAINT is_ticket_unique UNIQUE (Event_ID, Tier_ID, Seat_ID)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Fanclub_Membership`
--
DROP TABLE IF EXISTS `Fanclub_Membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fanclub_Membership` (
    `Membership_ID` INT(11) NOT NULL AUTO_INCREMENT,
    `Fan_ID` INT NOT NULL,
    `Fanclub_ID` INT NOT NULL,
    `Date_Joined` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`Membership_ID`),
    UNIQUE (`Fan_ID`, `Fanclub_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Artist_Follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Artist_Follower` (
	`Artist_ID` INT(11) NOT NULL,
    `Fan_ID` INT(11) NOT NULL, 
    
    PRIMARY KEY (`Artist_ID`, `Fan_ID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
