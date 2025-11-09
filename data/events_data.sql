-- 1. Temporarily disable foreign key checks
-- SET foreign_key_checks = 0;
-- TRUNCATE TABLE Seat;
-- 2. Truncate the table
-- TRUNCATE TABLE Ticket_Tier;
-- TRUNCATE TABLE Section;
-- TRUNCATE TABLE Tier_Section;
-- 3. Re-enable foreign key checks
-- SET foreign_key_checks = 1;

-- hello testt

INSERT INTO Venue (Venue_Name, City, Country, Capacity) 
VALUES  ("Philippine Arena", "Bocaue, Bulacan", "Philippines", 55000),
        ("SM Mall of Asia Arena", "Pasay, Metro Manila", "Philippines", 20000),
        ("Smart Araneta Coliseum", "Quezon City, Metro Manila", "Philippines", 16500),
        ("New Frontier Theater", "Quezon City, Metro Manila", "Philippines", 2385);

INSERT INTO Event (Event_Name, Event_Type, Venue_ID, Start_Date, End_Date, Start_Time, End_Time)
VALUES  ('BLACKPINK Comeback Tour', 'Concert', 1, '2026-08-10', '2026-08-11', '20:00:00', '00:00:00'),
        ('ENHYPEN Dunkin Donut Collab x Fanmeet', 'Fanmeet', 4, '2026-09-05', '2026-09-05', '14:00:00', '16:30:00'),
        ('ZB1 Hi-Five Session', 'Hi Touch', 3, '2026-10-18', '2026-10-18', '11:00:00', '13:00:00'),
        ('AKMU Birthday Cupsleeve Cafe', 'Cupsleeve', 4, '2026-11-25', '2026-11-25', '10:00:00', '17:00:00'),
        ('AESPA Artist Showcase', 'Concert,Fanmeet,Hi Touch', 2, '2026-12-07', '2026-12-07', '18:30:00', '22:30:00'),
        ("BLINKS United Rosé Birthday Cupsleeve", "Cupsleeve", 4, "2026-02-11", "2026-02-11", "9:00:00", "20:00:00"),
		("Zerose Squad Anniversary Cupsleeve", "Cupsleeve", 4, "2026-07-10", "2026-07-10", "10:00:00", "19:00:00"),
		("WinRina 4ever Winter Cupsleeve Cafe", "Cupsleeve", 4, "2026-01-15", "2026-01-15", "9:30:00", "18:30:00"),
		("ENGENE-ers Sunghoon Birthday Cupsleeve", "Cupsleeve", 4, "2026-12-08", "2026-12-08", "10:00:00", "20:00:00"),
		("Pink Venom Club Jisoo Cupsleeve", "Cupsleeve", 4, "2026-01-03", "2026-01-03", "9:00:00", "19:00:00"),
		("MY Dreams Karina Birthday Cupsleeve", "Cupsleeve", 4, "2026-04-11", "2026-04-11", "10:00:00", "18:00:00"),
		("Tokki Squad Hanni Cupsleeve Event", "Cupsleeve", 4, "2026-10-06", "2026-10-06", "9:30:00", "19:30:00"),
		("AKKADEMY Chanhyuk Birthday Cupsleeve", "Cupsleeve", 4, "2026-09-12", "2026-09-12", "10:00:00", "17:00:00"),
		("Bunnies Forever Hyein Cupsleeve", "Cupsleeve", 4, "2026-04-21", "2026-04-21", "9:00:00", "18:00:00"),
		("ENGENE Nation Jungwon Cupsleeve", "Cupsleeve", 4, "2026-02-09", "2026-02-09", "10:00:00", "19:00:00"),
		("Zero Days Hanbin Birthday Cupsleeve", "Cupsleeve", 4, "2026-01-16", "2026-01-16", "9:30:00", "20:00:00"),
		("BP World Lisa Birthday Cupsleeve", "Cupsleeve", 4, "2026-03-27", "2026-03-27", "10:00:00", "19:00:00"),
		("Next Level Fans Winter Cupsleeve", "Cupsleeve", 4, "2026-02-20", "2026-02-20", "9:00:00", "18:00:00"),
		("WIZONE Forever Sakura Cupsleeve", "Cupsleeve", 4, "2026-03-19", "2026-03-19", "10:00:00", "19:00:00"),
		("Bunny Camp Minji Birthday Cupsleeve", "Cupsleeve", 4, "2026-05-07", "2026-05-07", "9:30:00", "19:30:00"),
		("BLINK Paradise Jennie Cupsleeve", "Cupsleeve", 4, "2026-01-16", "2026-01-16", "10:00:00", "20:00:00"),
		("Vampire Lovers Heeseung Cupsleeve", "Cupsleeve", 4, "2026-10-15", "2026-10-15", "9:00:00", "18:00:00"),
		("ZB1 United Jiwoong Birthday Cupsleeve", "Cupsleeve", 4, "2026-12-14", "2026-12-14", "10:00:00", "19:00:00"),
		("Aespa Synk Ningning Cupsleeve", "Cupsleeve", 4, "2026-10-23", "2026-10-23", "9:30:00", "18:30:00"),
		("Suhyun & Chanhyuk Fans Anniversary Cupsleeve", "Cupsleeve", 4, "2026-04-19", "2026-04-19", "10:00:00", "17:00:00");
	
INSERT INTO Ticket_Tier(Tier_ID, Event_ID, Tier_Name, Price, Total_Quantity, Benefits, Is_Reserved_Seating)      
VALUES  (1, 1, 'VIP Pit', 15125.00, 1000, 'Early Entry, Sound Check Access', 1),
		(2, 1, 'Lower Bowl Premium', 11550.00, 4000, 'Priority Entry, Exclusive Photocard', 1),
		(3, 1, 'Lower Bowl Regular', 9900.00, 5000, 'Souvenir Ticket', 1),
		(4, 1, 'Upper Bowl', 6600.00, 8000, 'Standard Seating', 1),
		(5, 1, 'General Admission', 4950.00, 2000, 'Upper General Admission', 0),
		(6, 2, 'VIP Package', 9900.00, 500, 'Group Photo Raffle, Signed Poster', 1),
		(7, 2, 'Loge Seating', 6600.00, 700, 'Exclusive Merch Item', 1),
		(8, 2, 'Floor General Admission', 4400.00, 885, 'Standard Standing', 0),
		(9, 2, 'Balcony General Admission', 2750.00, 300, 'General Admission', 0),
		(10, 3, 'Hi-Touch VIP', 8250.00, 1500, 'Hi-Five Session, Signed Photocard', 1),
		(11, 3, 'Patron', 5500.00, 2500, 'Exclusive Photocard', 1),
		(12, 3, 'General Admission', 3850.00, 8500, 'Standard Seating', 0),
		(13, 4, 'Birthday Package', 1925.00, 500, 'Special Cupsleeve Set, Raffle Entry', 1),
		(14, 4, 'Cupsleeve Set', 1100.00, 1000, 'Standard Cupsleeve, Drink/Snack Voucher', 0),
		(15, 4, 'General Entry', 0.00, 800, 'General Admission (Must Purchase Drink)', 0),
		(16, 5, 'Showcase VIP', 13750.00, 1500, 'Sound Check, Group Photo Raffle', 1),
		(17, 5, 'Lower Box Premium', 9900.00, 4000, 'Exclusive Lanyard and Ticket Holder', 1),
		(18, 5, 'Upper Box', 6600.00, 5000, 'Souvenir Ticket', 0),
		(19, 5, 'General Admission', 4950.00, 2000, 'Standard General Admission', 0);

INSERT INTO Section(Venue_ID, Section_Name, Max_Capacity)
VALUES	(1, 'Lower Bowl', 25000),
		(1, 'Upper Bowl', 20000),
		(1, 'VIP Suites', 5000),
		(1, 'General Admission', 5000),
		(2, 'VIP', 2000),
		(2, 'Lower Box', 8000),
		(2, 'Upper Box', 7000),
		(2, 'General Admission', 3000),
		(3, 'Patron', 3000),
		(3, 'Lower Box', 5000),
		(3, 'Upper Box A', 4000),
		(3, 'Upper Box B / Gallery', 4500),
		(4, 'Floor General Admission', 885),
		(4, 'Loge Seating', 700),
		(4, 'Balcony General Admission', 800);

INSERT INTO Tier_Section (Tier_ID, Section_ID)
VALUES	(1, 3),   (2, 1),	(3, 1),
		(4, 2),   (5, 4),   (6, 15),
		(7, 14),  (8, 13),  (9, 15),
		(10, 9),  (10, 10), (11, 9),
		(12, 11), (12, 12),	(13, 13),
		(13, 14), (14, 13), (14, 14),
		(15, 15), (16, 5),  (17, 6),
		(18, 7),  (19, 8),
        (20, 13), (20, 14), (20, 15), 
		(21, 13), (21, 14), (21, 15), 
		(22, 13), (22, 14), (22, 15), 
		(23, 13), (23, 14), (23, 15), 
		(24, 13), (24, 14), (24, 15), 
		(25, 13), (25, 14), (25, 15), 
		(26, 13), (26, 14), (26, 15), 
		(27, 13), (27, 14), (27, 15), 
		(28, 13), (28, 14), (28, 15), 
		(29, 13), (29, 14), (29, 15), 
		(30, 13), (30, 14), (30, 15), 
		(31, 13), (31, 14), (31, 15), 
		(32, 13), (32, 14), (32, 15), 
		(33, 13), (33, 14), (33, 15), 
		(34, 13), (34, 14), (34, 15), 
		(35, 13), (35, 14), (35, 15), 
		(36, 13), (36, 14), (36, 15), 
		(37, 13), (37, 14), (37, 15), 
		(38, 13), (38, 14), (38, 15), 
		(39, 13), (39, 14), (39, 15);

-- select * from tier_section;
-- select * FROM ticket_tier
-- order by tier_id;

-- SELECT * FROM Seat
-- WHERE Section_ID IN (
--     SELECT Section_ID FROM Section WHERE Section_ID = 2
-- )
-- ORDER BY Seat_ID;
