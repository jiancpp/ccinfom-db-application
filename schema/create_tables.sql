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
-- Table structure for table `artists`
--
DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `debut_date` DATE NOT NULL,
    `fanclub_members` INT NOT NULL DEFAULT 0,  -- need ba toh dito or aggregation na lang sa view
    PRIMARY KEY (`id`)
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
-- Table structure for `events`
--
DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(100) NOT NULL,
    `type` SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve') NOT NULL,
    `artist_id` INT,
    `fanclub_id` INT,
    `venue_id` INT NOT NULL,
    `event_date` DATETIME NOT NULL,
    `description` VARCHAR(255) NOT NULL,

    PRIMARY KEY (`id`),
    -- FOREIGN KEY (`artist_id`) REFERENCES artists(`id`),
    -- FOREIGN KEY (`fanclub_id`) REFERENCES fanclubs(`id`),
    -- FOREIGN KEY (`venue_id`) REFERENCES venues(`id`),
    UNIQUE (`venue_id`, `event_date`)
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
-- Table structure for `venues`
--
DROP TABLE IF EXISTS `venues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venues` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL, 
    `location` VARCHAR(255) NOT NULL, 
    `capacity` INT NOT NULL CHECK (capacity > 0),
    
    PRIMARY KEY (`id`),
    UNIQUE (`name`, `location`) -- Prevents duplicate venues with the same name and location
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seats`
--
DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
    `venue_id` INT(11) NOT NULL,
    `section` VARCHAR(100) NOT NULL,
    `row_number` VARCHAR(5) NOT NULL, 
    `seat_number` VARCHAR(5) NOT NULL,
    
    PRIMARY KEY (`id`),
	UNIQUE (`venue_id`, `section`, `row_number`, `seat_number`) -- Prevents duplicates of the seat

    -- FOREIGN KEY (`venue_id`) REFERENCES venues(`id`)
	-- 	ON DELETE CASCADE ON UPDATE CASCADE,
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for `ticket_tier`
--
DROP TABLE IF EXISTS `ticket_tier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_tier` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `tier_name` VARCHAR(100) NOT NULL DEFAULT 'General Admissions',
    `price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `total_quantity` INT NOT NULL DEFAULT 0,
    `quantity_sold` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    UNIQUE (`event_id`, `tier_name`)
    -- FOREIGN KEY (`event_id`) REFERENCES events(`id`),
    -- -- Ensures that there is enough slots available
    -- CONSTRAINT check_qty CHECK (`quantity_sold` <= `total_quantity`)
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
-- Table structure for `ticket_sales`
--
DROP TABLE IF EXISTS `ticket_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_sales` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `event_id` INT NOT NULL,
    `tier_id` INT NOT NULL,
    `seat_id` INT,
    `purchase_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`)
    -- FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    -- FOREIGN KEY (`event_id`) REFERENCES events(`id`),
    -- FOREIGN KEY (`tier_id`) REFERENCES ticket_tier(`id`),
    -- FOREIGN KEY (`seat_id`) REFERENCES seats(`id`),

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




