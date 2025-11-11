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
(6, 'BLACKPINK Official Light Stick Special Edition', 1, NULL, NULL, '', 2000, 1000, 1000),
(7, 'BLACKPINK Airpods Silicone Case Set', 1, NULL, NULL, '', 850, 1000, 1000),
(8, 'ENHYPEN X Dunkin'' Tumbler', 2, 2, NULL, '450 ML tumbler with ENHYPEN x Dunkin’ design', 750, 500, 500),
(9, 'ENHYPEN X Dunkin'' Tote Bag', 2, 2, NULL, 'Eco tote bag featuring Dunkin’ logo and members', 450, 500, 500),
(10, 'ENHYPEN X Dunkin'' Tin Case', 2, 2, NULL, 'Metal tin case for storing photocard sets', 250, 500, 500),
(11, 'ENHYPEN X Dunkin'' Collector''s Set', 2, 2, NULL, 'Complete set with photocard, tote, and tumbler', 1000, 600, 600),
(12, 'ZB1 Hi-Five Polaroid Set', 3, 3, 6, 'Instant film set with members’ printed signatures', 600, 400, 400),
(13, 'ZB1 Keyring', 3, 3, 6, 'Official ZB1 acrylic keyring with nameplate', 1000, 700, 700),
(14, 'AKMU Birthday Mug', 4, 4, NULL, 'Ceramic mug celebrating AKMU’s birthday cafe event', 500, 500, 500),
(15, 'AKMU Cupsleeve Set', 4, 4, NULL, 'Collectible cupsleeves from AKMU’s cafe event', 950, 600, 600),
(16, 'AESPA Mini Poster', 5, 5, NULL, 'Limited edition A4 poster from showcase', 800, 700, 700),
(17, 'AESPA Karina Photocard Set', 5, 5, NULL, 'Karina exclusive photocard pack', 850, 800, 800),
(18, 'AESPA Winter Photocard Set', 5, 5, NULL, 'Winter exclusive photocard pack', 850, 800, 800),
(19, 'AESPA Giselle Photocard Set', 5, 5, NULL, 'Giselle exclusive photocard pack', 850, 800, 800),
(20, 'AESPA Ningning Photocard Set', 5, 5, NULL, 'Ningning exclusive photocard pack', 850, 800, 800);
