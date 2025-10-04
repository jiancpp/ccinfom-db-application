CREATE DATABASE IF NOT EXISTS `dbApp`;
USE `dbApp`;

--
-- Table structure for `events`
-- 

DROP TABLE IF EXISTS `events`;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `artist_id` INT NOT NULL,
    `fanclub_id` INT,
    `title` VARCHAR(100) NOT NULL,
    `type` SET('Concert', 'Fanmeet', 'Hi Touch', 'Cupsleeve') NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `venue_id` INT NOT NULL,
    `event_date` DATETIME NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`artist_id`) REFERENCES artist(`id`),
    FOREIGN KEY (`fanclub_id`) REFERENCES fanclub(`id`),
    FOREIGN KEY (`venue_id`) REFERENCES venue(`id`)
);

--
-- Table structure for `venue`
--

DROP TABLE IF EXISTS `venue`;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venue` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `venue_name` VARCHAR(100) NOT NULL UNIQUE,
    `location` VARCHAR(100) NOT NULL,
    `capacity` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
);

--
-- Table structure for `seat`
--

DROP TABLE IF EXISTS `seat`;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seat` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `venue_id` INT NOT NULL,
    `section` VARCHAR(100) DEFAULT '',
    `row_number` INT(3) NOT NULL,
    `seat_number` INT(3) NOT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`venue_id`) REFERENCES venue(`id`),

    UNIQUE (venue_id, section, row_number, seat_number)
);

--
-- Table structure for `ticket_tier`
--

DROP TABLE IF EXISTS `ticket_tier`;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_tier` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `tier_name` VARCHAR(100) NOT NULL DEFAULT 'General Admissions',
    `price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `total_quantity` INT NOT NULL DEFAULT 0,
    `quantity_sold` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`event_id`) REFERENCES events(`id`),

    -- Ensures that there is enough slots available
    CONSTRAINT check_qty CHECK (`quantity_sold` <= `total_quantity`)
);


--
-- Table structure for `ticket_sales`
--

DROP TABLE IF EXISTS `ticket_sales`;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_sales` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `event_id` INT NOT NULL,
    `tier_id` INT NOT NULL,
    `seat_id` INT,
    `purchase_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    FOREIGN KEY (`event_id`) REFERENCES events(`id`),
    FOREIGN KEY (`tier_id`) REFERENCES ticket_tier(`id`),
    FOREIGN KEY (`seat_id`) REFERENCES seat(`id`),

    -- Ensures that only one seat per event and tier is sold 
    -- (works for free seating where seat is NULL)
    CONSTRAINT is_ticket_unique UNIQUE (event_id, tier_id, seat_id)
);