-- 1. MANAGER TABLE (Parent)
INSERT INTO Manager (Manager_ID, Manager_Name, Contact_Num, Contact_Email, Agency_Address) VALUES
(1, 'Kim Min-jun', '01012345678', 'm.kim@ygmail.com', 'YG Building, 12, Hapjeong-ro, Mapo-gu, Seoul, South Korea'),
(2, 'Sejin', '01098765432', 's.jin@gmail.com', 'Belift Lab, 42, Hangang-daero, Yongsan-gu, Seoul, South Korea'),
(3, 'Park Seo-joon', '01022446688', 's.park@wakeone.com', 'WakeOne Tower, 7, World Cup buk-ro 58-gil, Mapo-gu, Seoul, South Korea'),
(4, 'Choi Eun-woo', '01013572468', 'e.choi@ygmail.com', 'YG Building, 12, Hapjeong-ro, Mapo-gu, Seoul, South Korea'),
(5, 'Jung Ha-yoon', '01055117733', 'h.jung@smtown.com', 'SM Entertainment, 83-21, Wangsimni-ro, Seongdong-gu, Seoul, South Korea'),
(6, 'Kang Ji-hyun', '01086420975', 'j.kang@ador.world', '10F, ADOR, 42, Hangang-daero, Yongsan-gu, Seoul, South Korea'),
(7, 'Han Sung-min', '01031415926', 's.han@offtherecord.co.kr', 'OTR Entertainment, 22, Dosan-daero 16-gil, Gangnam-gu, Seoul, South Korea');

-- 2. ARTIST TABLE (Parent, references Manager)
INSERT INTO Artist (Artist_ID, Manager_ID, Artist_Name, Activity_Status, Debut_Date) VALUES
(1, 1, 'BlackPink', 'Active', '2016-08-08'),
(2, 2, 'Enhyphen', 'Active', '2020-11-30'),
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

-- 4. NATIONALITY TABLE (Child, references Member)
INSERT INTO Nationality (Nationality_ID, Nationality_Name) VALUES
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

-- 5. MEMBER_NATIONALITY TABLE (Junction, references Member and Nationality)
INSERT INTO Member_Nationality (Member_ID, Nationality_ID) VALUES
(1, 1), (2, 1), (3, 2), (4, 3), (5, 1), (6, 1), (7, 1), (7, 4), (8, 1), (8, 5),
(9, 1), (10, 1), (11, 6), (12, 1), (13, 7), (14, 1), (15, 1), (16, 1), (17, 7),
(18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1), (24, 6), (24, 1), (25, 1),
(26, 7), (27, 1), (28, 9), (28, 5), (29, 1), (29, 5), (30, 1), (31, 1), (32, 1),
(33, 6), (34, 1), (35, 1), (36, 1), (37, 1), (38, 1), (39, 6), (40, 6), (41, 1),
(42, 1), (43, 1), (44, 1), (45, 6), (46, 1), (47, 6), (48, 1), (49, 1), (50, 1),
(51, 1), (52, 1), (53, 4), (53, 1), (54, 7), (55, 1), (56, 1), (57, 1), (58, 1),
(59, 1), (60, 7), (61, 1), (62, 4), (62, 1), (63, 1), (64, 1), (65, 6), (66, 10),
(67, 6), (68, 1), (69, 10), (70, 1), (71, 1);

-- 6. ROLE TABLE () (Child, references Member)
INSERT INTO Role (Role_ID, Role_Name) VALUES
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

-- 7. MEMBER_ROLE TABLE (Child, references Member)
INSERT INTO Member_Role (Member_ID, Role_ID) VALUES
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
(3, 30),
(3, 31),
(2, 31),
(5, 31);

-- 9. ARTIST_FOLLOWER TABLE (Junction, references Artist and Fan)
-- NOTE: Assuming 'Fan' records are already inserted or the table is not required to be inserted first.
INSERT INTO Artist_Follower (Artist_ID, Fan_ID) VALUES
(5, 1),
(7, 1),
(6, 2),
(1, 3),
(10, 3),
(2, 4),
(1, 5),
(5, 6),
(10, 7),
(11, 8);

-- 10. SETLIST TABLE (Junction, references Artist and Event)
INSERT INTO Setlist (Artist_ID, Event_ID, Song_Name, Play_Order) VALUES
(1, 1, 'Pink Venom', 1),
(1, 1, 'How You Like That', 2),
(1, 1, 'Shut Down', 3),
(1, 1, 'DDU-DU DDU-DU', 4),
(1, 1, 'Kill This Love', 5),
(1, 1, 'As If It''s Your Last', 6),
(2, 2, 'Drunk-Dazed', 1),
(2, 2, 'Sweet Venom', 2),
(2, 2, 'Polaroid Love', 3),
(2, 2, 'Bite Me', 4),
(3, 3, 'In Bloom', 1),
(3, 3, 'CRUSH', 2),
(5, 5, 'Black Mamba', 1),
(5, 5, 'Next Level', 2),
(5, 5, 'Savage', 3),
(5, 5, 'Drama', 4),
(5, 5, 'Supernova', 5);