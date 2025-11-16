use dbapp;

INSERT INTO Merchandise (
    Merchandise_ID, 
    Merchandise_Name,
    Artist_ID,
    Event_ID,
    Fanclub_ID,
    Merchandise_Description,
    Merchandise_Price, 
    Initial_Stock,
    Quantity_Stock
) VALUES
(1, 'BLACKPINK World Tour Tee Black', 1, 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a black heavyweight unisex tee.', 4000, 500, 500),
(2, 'BLACKPINK World Tour Tee White', 1, 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a white heavyweight unisex tee.', 4000, 500, 500),
(3, 'BLACKPINK Sticker Set', 1, 1, NULL, 'Includes 1 BLACKPINK logo sticker, 1 Deadline Tour logo sticker, 1 Heart logo sticker, 1 Black heart sticker with BLACKPINK in the middle, 1 Character sticker', 800, 600, 600),
(4, 'BLACKPINK Foil Zip Hoodie White', 1, 1, NULL, 'BLACKPINK Deadline World Tour printed on the front and cities printed on the back of a white unisex zip hoodie.', 7900, 300, 300),
(5, 'BLACKPINK Cuff Beanie Black', 1, 1, NULL, 'Black cuff beanie with BLACKPINK embroidered on the front in pink thread.', 2800, 300, 300),
(6, 'BLACKPINK Official Light Stick Special Edition', 1, NULL, NULL, 'The BLACKPINK Official Light Stick Special Edition is an upgraded, premium version of the group’s signature hammer light stick, featuring improved design and enhanced functionality.', 2000, 1000, 1000),
(7, 'BLACKPINK Airpods Silicone Case Set', 1, NULL, NULL, 'The BLACKPINK AirPods Silicone Case Set is a stylish, protective accessory featuring the group’s signature design for a sleek and durable AirPods cover.', 850, 1000, 1000),
(8, 'ENHYPEN X Dunkin'' Tumbler', 2, 2, NULL, '450 ML tumbler with ENHYPEN x Dunkin’ design', 750, 500, 500),
(9, 'ENHYPEN X Dunkin'' Tote Bag', 2, 2, NULL, 'Eco tote bag featuring Dunkin’ logo and members', 450, 500, 500),
(10, 'ENHYPEN X Dunkin'' Tin Case', 2, 2, NULL, 'Metal tin case for storing photocard sets', 250, 500, 500),
(11, 'ENHYPEN X Dunkin'' Collector''s Set', 2, 2, NULL, 'Complete set with photocard, tote, and tumbler', 1000, 600, 600),
(12, 'ZB1 Hi-Five Polaroid Set', 3, 3, NULL, 'Instant film set with members’ printed signatures', 600, 400, 400),
(13, 'ZB1 Keyring', 3, 3, NULL, 'Official ZB1 acrylic keyring with nameplate', 1000, 700, 700),
(14, 'AKMU Birthday Mug', NULL, 4, 3, 'Ceramic mug celebrating AKMU’s birthday cafe event', 500, 500, 500),
(15, 'AKMU Cupsleeve Set', NULL, 4, 24, 'Collectible cupsleeves from AKMU’s cafe event', 950, 600, 600),
(16, 'AESPA Mini Poster', 5, 5, NULL, 'Limited edition A4 poster from showcase', 800, 700, 700),
(17, 'AESPA Karina Photocard Set', 5, 5, NULL, 'Karina exclusive photocard pack', 850, 800, 800),
(18, 'AESPA Winter Photocard Set', 5, 5, NULL, 'Winter exclusive photocard pack', 850, 800, 800),
(19, 'AESPA Giselle Photocard Set', 5, 5, NULL, 'Giselle exclusive photocard pack', 850, 800, 800),
(20, 'AESPA Ningning Photocard Set', 5, 5, NULL, 'Ningning exclusive photocard pack', 850, 800, 800),


(21, 'Rosé Birthday Cupsleeve Set', NULL, 6, 4, 'Includes collectible cupsleeve, postcard, and sticker set for Rosé’s birthday event.', 500, 400, 400),
(22, 'Rosé Birthday Photocard', 1, 4, NULL, 'Limited edition Rosé birthday photocard.', 150, 600, 600),

-- Event 7: Zerose Squad Anniversary Cupsleeve
(23, 'ZB1 Anniversary Cupsleeve Set', NULL, 7, 6, 'Includes collectible cupsleeve, holographic photocard, and pin badge for ZB1 anniversary.', 600, 500, 500),
(24, 'ZB1 Group Sticker Sheet', NULL, 7, 6, 'Vinyl sticker sheet with ZB1 members and logo for the anniversary.', 250, 700, 700),

-- Event 8: WinRina 4ever Winter Cupsleeve Cafe
(25, 'WinRina Winter Cupsleeve Set', NULL, 8, 2, 'Includes collectible cupsleeve, A5 art print, and keychain for the WinRina winter event.', 750, 450, 450),
(26, 'WinRina Photostrip', NULL, 8, 2, 'Set of two themed photostrips featuring Karina and Winter.', 200, 600, 600),

-- Event 9: ENGENE-ers Sunghoon Birthday Cupsleeve
(27, 'Sunghoon Birthday Cupsleeve Kit', NULL, 9, 5, 'Includes collectible cupsleeve, mini banner, and customized fan.', 550, 400, 400),
(28, 'Sunghoon Acrylic Standee', NULL, 9, 5, 'Sunghoon birthday themed acrylic standee.', 850, 300, 300),

-- Event 10: Pink Venom Club Jisoo Cupsleeve
(29, 'Jisoo Birthday Cupsleeve Package', NULL, 10, 10, 'Includes collectible cupsleeve, glitter photocard, and button pin for Jisoo’s birthday.', 500, 500, 500),
(30, 'Jisoo Pop Socket', NULL, 10, 10, 'Custom Jisoo birthday themed pop socket.', 300, 500, 500),

-- Event 11: MY Dreams Karina Birthday Cupsleeve
(31, 'Karina Birthday Cupsleeve Set', NULL, 11, 7, 'Includes collectible cupsleeve, exclusive birthday bookmark, and wristband.', 450, 400, 400),
(32, 'Karina Birthday Lanyard', NULL, 11, 7, 'Themed lanyard with Karina’s birthday design.', 350, 500, 500),

-- Event 12: Tokki Squad Hanni Cupsleeve Event (Assuming Hanni is from a group not in the provided data, assigning a hypothetical Artist_ID=6, Fanclub_ID=5)
(33, 'Hanni Cupsleeve Set', NULL, 12, 17, 'Includes collectible cupsleeve, lenticular card, and themed decal sticker.', 550, 450, 450),
(34, 'Hanni Mini Washi Tape', NULL, 12, 17, 'Mini roll of decorative washi tape featuring Hanni.', 200, 600, 600),

-- Event 13: AKKADEMY Chanhyuk Birthday Cupsleeve
(35, 'Chanhyuk Birthday Cupsleeve Set', NULL, 13, 3, 'Includes collectible cupsleeve, special photocard, and Chanhyuk-themed doodle magnet.', 500, 350, 350),
(36, 'AKMU Lyrics Postcard Set', NULL, 13, 3, 'Set of 4 postcards featuring AKMU song lyrics.', 400, 400, 400),

-- Event 14: Bunnies Forever Hyein Cupsleeve (Assuming Hyein is from the same group as Hanni, Artist_ID=6, Fanclub_ID=5)
(37, 'Hyein Cupsleeve Kit', NULL, 14, 8, 'Includes collectible cupsleeve, polaroid print set, and keyring charm.', 600, 400, 400),
(38, 'Hyein Hair Clip Set', NULL, 14, 8, 'Set of two themed hair clips.', 350, 500, 500),

-- Event 15: ENGENE Nation Jungwon Cupsleeve
(39, 'Jungwon Birthday Cupsleeve Set', NULL, 15, 11, 'Includes collectible cupsleeve, birthday postcard, and holographic sticker.', 450, 500, 500),
(40, 'Jungwon Fabric Poster', NULL, 15, 11, 'Small fabric poster with Jungwon’s birthday design.', 600, 300, 300),

-- Event 16: Zero Days Hanbin Birthday Cupsleeve
(41, 'Hanbin Birthday Cupsleeve Package', NULL, 16, 1, 'Includes collectible cupsleeve, lenticular photocard, and special member badge.', 550, 450, 450),
(42, 'Hanbin Photo Film Strip', NULL, 16, 1, 'Set of two Hanbin-themed photo film strips.', 200, 600, 600),

-- Event 17: BP World Lisa Birthday Cupsleeve
(43, 'Lisa Birthday Cupsleeve Set', NULL, 17, 15, 'Includes collectible cupsleeve, exclusive sticker pack, and photostrip.', 500, 400, 400),
(44, 'Lisa Pin Badge', NULL, 17, 15, 'Custom design Lisa birthday pin badge.', 250, 500, 500),

-- Event 18: Next Level Fans Winter Cupsleeve
(45, 'Winter Cupsleeve Set', NULL, 18, 25, 'Includes collectible cupsleeve, special keyring, and mini-fan.', 600, 350, 350),
(46, 'Winter Photocard Set (Fanmade)', NULL, 18, 25, 'Set of 5 fanmade photocards of Winter.', 400, 400, 400),

-- Event 19: WIZONE Forever Sakura Cupsleeve (Assuming Sakura is from a group not in the provided data, assigning a hypothetical Artist_ID=7, Fanclub_ID=6)
(47, 'Sakura Cupsleeve Package', NULL, 19, 27, 'Includes collectible cupsleeve, mini-poster, and reflective sticker.', 500, 400, 400),
(48, 'Sakura ID Photocard', NULL, 19, 27, 'Sakura ID style photocard.', 150, 600, 600),

-- Event 20: Bunny Camp Minji Birthday Cupsleeve (Assuming Minji is from the same group as Hanni/Hyein, Artist_ID=6, Fanclub_ID=5)
(49, 'Minji Birthday Cupsleeve Kit', NULL, 20, 26, 'Includes collectible cupsleeve, 4-cut photostrip, and custom bookmark.', 500, 450, 450),
(50, 'Minji Rabbit Plushie Keychain', NULL, 20, 26, 'Small plushie keychain with a rabbit design.', 700, 300, 300),

-- Event 21: BLINK Paradise Jennie Cupsleeve
(51, 'Jennie Birthday Cupsleeve Set', NULL, 21, 21, 'Includes collectible cupsleeve, quote postcard, and themed sticker sheet.', 500, 500, 500),
(52, 'Jennie Mini Polaroid Set', NULL, 21, 21, 'Set of 3 mini polaroid prints of Jennie.', 250, 500, 500),

-- Event 22: Vampire Lovers Heeseung Cupsleeve
(53, 'Heeseung Cupsleeve Set', NULL, 22, 22, 'Includes collectible cupsleeve, exclusive photocard, and themed art print.', 550, 400, 400),
(54, 'Heeseung Fanmade Bracelet', NULL, 22, 22, 'Beaded bracelet with Heeseung’s name/initials.', 300, 350, 350),

-- Event 23: ZB1 United Jiwoong Birthday Cupsleeve
(55, 'Jiwoong Birthday Cupsleeve Package', NULL, 23, 23, 'Includes collectible cupsleeve, birthday slogan, and photocard.', 500, 450, 450),
(56, 'Jiwoong Photo Binder', NULL, 23, 23, 'Small A5 photo binder for photocards.', 800, 300, 300),

-- Event 24: Aespa Synk Ningning Cupsleeve
(57, 'Ningning Cupsleeve Set', NULL, 24, 14, 'Includes collectible cupsleeve, postcard set, and holographic sticker.', 450, 400, 400),
(58, 'Ningning Pop-up Photocard', NULL, 24, 14, '3D Pop-up photocard of Ningning.', 200, 500, 500),

-- Event 25: Suhyun & Chanhyuk Fans Anniversary Cupsleeve
(59, 'AKMU Anniversary Cupsleeve Duo Set', NULL, 25, 20, 'Includes two collectible cupsleeves (Suhyun and Chanhyuk), and a special anniversary photocard.', 700, 400, 400),
(60, 'AKMU Logo Tote Bag (Fanmade)', NULL, 25, 20, 'Small fanmade tote bag with AKMU logo and anniversary text.', 550, 300, 300),

-- Event 26: IU Concert: Blooming in Blue (Assuming IU has Artist_ID=8, Fanclub_ID=7)
(61, 'IU Blooming in Blue Concert Tee', 8, 26, NULL, 'Official concert t-shirt in blue, with tour name and dates.', 3500, 800, 800),
(62, 'IU Official Light Stick Ver. 3', 8, 26, NULL, 'IU’s official light stick, the third version.', 2500, 1500, 1500),
(63, 'IU Photo Slogan', 8, 26, NULL, 'Large fabric slogan with IU’s photo and name.', 900, 1000, 1000),

-- Event 27: IZNA Anniversary Fanmeet 
(64, 'IZNA Anniversary Slogan Towel', 7, 27, NULL, 'Small commemorative hand towel with IZNA anniversary logo.', 700, 500, 500),
(65, 'IZNA Unit Photocard Set', 7, 27, NULL, 'Set of unit photocards from the anniversary fanmeet.', 800, 600, 600),

-- Event 28: LISA: Lovesick Concert
(66, 'LISA Lovesick Tour Hoodie', 1, 28, NULL, 'Official black hoodie with LISA Lovesick Tour logo.', 7500, 400, 400),
(67, 'LISA Photo Card Binder', 1, 28, NULL, 'Small photo card collector binder, black and gold themed.', 1500, 500, 500),
(68, 'LISA Lovesick Official Light Stick Topper', 1, 28, NULL, 'Interchangeable topper for the BLACKPINK light stick with a LISA design.', 1000, 700, 700),

-- Event 29: SEVENTEEN Comeback Tour (Assuming SEVENTEEN has Artist_ID=9, Fanclub_ID=8)
(69, 'SEVENTEEN Tour T-Shirt', 10, 29, NULL, 'Official tour t-shirt with comeback theme.', 4000, 800, 800),
(70, 'SEVENTEEN Cheering Kit', 10, 29, NULL, 'Includes slogan, banner, and cheering accessories.', 1200, 1000, 1000),
(71, 'SEVENTEEN Official Light Stick Ver. 4', 10, 29, NULL, 'SEVENTEEN’s official light stick, the fourth version.', 2500, 1500, 1500),

-- Event 30: ZB1 Summer in Manila Concert
(72, 'ZB1 Summer Concert Tee', 3, 30, NULL, 'Light blue t-shirt with ZB1 Summer in Manila event logo.', 3800, 700, 700),
(73, 'ZB1 Photo Film Set (Concert Ver.)', 3, 30, NULL, 'Set of 5 film-style photocards from the concert.', 500, 800, 800),
(74, 'ZB1 Summer Concert Fan', 3, 30, NULL, 'Handheld electric fan with ZB1 logo.', 900, 600, 600),

-- Event 31: SB19 Asia Stage: Manila (Assuming SB19 has Artist_ID=10, Fanclub_ID=9)
(75, 'UNIS Asia Stage Official Hoodie', 11, 31, NULL, 'Black official hoodie from the Asia Stage event.', 4500, 500, 500),
(76, 'UNIS Light Stick Charm Set', 11, 31, NULL, 'Set of charms to decorate the official light stick.', 850, 700, 700),

(77, 'BLACKPINK Vinyl Record (The Album)', 1, NULL, NULL, 'Limited edition pink vinyl record of BLACKPINK’s first studio album.', 4500, 700, 700),
(78, 'BLINK Official Membership Kit', 1, NULL, NULL, 'The annual BLINK membership kit including a photobook, badge set, and member cards.', 3500, 1000, 1000),

-- ENHYPEN (Artist_ID: 2)
(79, 'ENHYPEN Logo Keychain', 2, NULL, NULL, 'Official acrylic keyring with ENHYPEN’s group logo.', 900, 800, 800),
(80, 'ENGENE Official Fan Kit 2026', 2, NULL, NULL, 'The official ENGENE annual fan kit with exclusive merchandise, photocard sets, and fanbook.', 4000, 1000, 1000),
(81, 'ENHYPEN World Tour Photo Essay', 2, NULL, NULL, 'Official photo essay book capturing behind-the-scenes moments from their recent world tour.', 2500, 600, 600),

-- ZEROBASEONE (ZB1) (Artist_ID: 3)
(82, 'ZB1 Debut Mini Photobook', 3, NULL, NULL, 'Mini photobook commemorating the group’s debut.', 1800, 800, 800),
(83, 'ZEROSE Official Membership Card', 3, NULL, NULL, 'Official physical membership card for the ZEROSE fanclub.', 1000, 2000, 2000),
(84, 'ZB1 Group Slogan Towel', 3, NULL, NULL, 'High-quality fabric slogan towel featuring all nine members.', 1100, 900, 900),

-- AKMU (Artist_ID: 4)
(85, 'AKMU Re-Imagined Album LP', 4, NULL, NULL, 'Vinyl LP record of AKMU’s re-imagined greatest hits album.', 5000, 500, 500),
(86, 'AKMU "Sailing" Poster Set', 4, NULL, NULL, 'Set of 4 official posters from the "Sailing" era.', 1200, 700, 700),
(87, 'AKMU Official Slogan Towel', 4, NULL, NULL, 'Official fabric slogan towel with AKMU’s logo and name.', 800, 900, 900),

-- AESPA (Artist_ID: 5)
(88, 'MY Official Membership Kit', 5, NULL, NULL, 'The annual MY membership kit including exclusive ID card, pin set, and stationary.', 3800, 1100, 1100),
(89, 'AESPA Logo Patch Set', 5, NULL, NULL, 'Set of embroidered patches featuring the AESPA and member logos.', 750, 900, 900),
(90, 'AESPA Synk Hyperline Blu-ray', 5, NULL, NULL, 'Concert Blu-ray disc of the Synk: Hyper Line world tour.', 4500, 500, 500),

-- NewJeans (Artist_ID: 6)
(91, 'Bunnies Official Membership Kit', 6, NULL, NULL, 'The annual Bunnies membership kit featuring exclusive photo cards and a tin case.', 3600, 1000, 1000),
(92, 'NewJeans 1st EP Bluebook Ver.', 6, NULL, NULL, 'The physical album release of NewJeans 1st EP (Bluebook Version).', 1500, 1500, 1500),
(93, 'NewJeans Bunny Keyring', 6, NULL, 5, 'Small metal keyring in the shape of the group’s signature rabbit logo.', 800, 1200, 1200),

-- IU (Artist_ID: 8)
(94, 'UAENA Official Fan Kit 2026', 8, NULL, NULL, 'The annual UAENA official fan kit with photocards, photobook, and fan-exclusive items.', 4200, 800, 800),
(95, 'IU Photo Slogan Set', 8, NULL, 7, 'Set of three high-quality fabric slogans featuring different IU photos.', 1500, 700, 700),
(96, 'IU Concert Merch T-Shirt (Generic)', 8, NULL, NULL, 'Simple, high-quality t-shirt with IU’s stylized name on the chest.', 2800, 600, 600),

-- SEVENTEEN (Artist_ID: 9)
(97, 'CARAT Official Membership Kit', 10, NULL, NULL, 'The annual CARAT membership kit with exclusive keyring, photobook, and badge.', 3900, 1000, 1000),
(98, 'SEVENTEEN Logo Hat', 10, NULL, NULL, 'Official baseball cap with the SEVENTEEN logo embroidered on the front.', 2500, 600, 600),
(99, 'SEVENTEEN 13 Member Photocard Pack', 10, NULL, NULL, 'Official photocard pack containing one card for each of the thirteen members.', 950, 1100, 1100),

-- SB19 (Artist_ID: 9)
(100, 'IZNA Official Membership Kit', 9, NULL, NULL, 'The official IZNA membership kit, including a personalized card and exclusive merch.', 3700, 900, 900),
(101, 'IZNA Group Photocard Pack', 9, NULL, NULL, 'Official photocard pack featuring all members of IZNA.', 650, 1200, 1200),
(102, 'IZNA Official Fan Towel', 9, NULL, NULL, 'Standard sized fan towel with the IZNA logo.', 900, 700, 700),

-- UNIS (Artist_ID: 11)
(103, 'UNIS Debut Album Pouch Set', 11, NULL, NULL, 'Pouch set released alongside UNIS’s debut album.', 1000, 800, 800),
(104, 'UNIS Logo Pin', 11, NULL, NULL, 'Enamel pin featuring the official UNIS logo.', 500, 1000, 1000);