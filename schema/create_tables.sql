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
    `Merchandise_Name` VARCHAR(100) NOT NULL,
    `Artist_ID` INT(11),
    `Event_ID` INT(11),
    `Fanclub_ID` INT(11),
    `Merchandise_Description` VARCHAR(500) DEFAULT NULL,
    `Merchandise_Price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `Initial_Stock` INT(6) NOT NULL DEFAULT 0,
    `Quantity_Stock` INT(6) NOT NULL DEFAULT 0,

    PRIMARY KEY (`Merchandise_ID`),
    UNIQUE (`Event_ID`, `Merchandise_Name`),

	CHECK (`Merchandise_Price` >= 0),
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
    `Venue_ID` INT(11) NOT NULL,
	`Start_Date` DATE NOT NULL,
	`End_Date` DATE NOT NULL,
	`Start_Time` TIME NOT NULL,
	`End_Time` TIME,

    PRIMARY KEY (`Event_ID`),
	CONSTRAINT is_valid_date CHECK(`Start_Date` <= `End_Date`),
    CONSTRAINT uk_venue_date UNIQUE(`Venue_ID`, `Start_Date`)
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
    `Order_Status` ENUM('Pending', 'Paid', 'Cancelled', 'Refunded') NOT NULL DEFAULT 'Pending',

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


