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