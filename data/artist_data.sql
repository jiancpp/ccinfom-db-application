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
INSERT INTO Artist (Artist_ID, Manager_ID, Artist_Name, Activity_Status, Debut_Date, Debut_Days) VALUES
(1, 1, 'BlackPink', 'Active', '2016-08-08', 3378),
(2, 2, 'Enhypen', 'Active', '2020-11-30', 1803),
(3, 3, 'Zerobaseone', 'Active', '2023-07-10', 851),
(4, 4, 'AKMU', 'Active', '2014-04-07', 4232),
(5, 5, 'Aespa', 'Active', '2020-11-27', 1806),
(6, 6, 'New Jeans', 'Hiatus', '2022-07-22', 1204),
(7, 7, 'Iz*One', 'Inactive', '2018-10-29', 2566);

-- 3. MEMBER_DETAIL TABLE (Child, references Artist)
INSERT INTO Member_Detail (Member_ID, Artist_ID, Member_Name, Role, Activity_Status, Nationality, Birth_Date, Age) VALUES
(1, 1, 'Kim Ji-soo', 'Vocalist, Visual', 'Active', 'South Korean', '1995-01-03', 30),
(2, 1, 'Jennie Kim', 'Rapper, Vocalist', 'Active', 'South Korean', '1996-01-16', 29),
(3, 1, 'Rosé Park', 'Vocalist, Dancer', 'Active', 'New Zealander', '1997-02-11', 28),
(4, 1, 'Lisa Manoban', 'Dancer, Rapper, Maknae', 'Active', 'Thai', '1997-03-27', 28),
(5, 2, 'Yang Jung-won', 'Leader, Vocalist, Dancer', 'Active', 'South Korean', '2004-02-09', 21),
(6, 2, 'Lee Hee-seung', 'Vocalist, Dancer', 'Active', 'South Korean', '2001-10-15', 24),
(7, 2, 'Jay Park', 'Rapper, Dancer, Vocalist', 'Active', 'South Korean / American', '2002-04-20', 23),
(8, 2, 'Jake Sim', 'Rapper, Vocalist', 'Active', 'South Korean / Australian', '2002-11-15', 22),
(9, 2, 'Park Sung-hoon', 'Vocalist, Dancer, Visual', 'Active', 'South Korean', '2002-12-08', 22),
(10, 2, 'Kim Sun-oo', 'Vocalist', 'Active', 'South Korean', '2003-06-24', 22),
(11, 2, 'Ni-ki', 'Dancer, Rapper, Maknae', 'Active', 'Japanese', '2005-12-09', 19),
(12, 3, 'Kim Ji-woong', 'Vocalist, Rapper', 'Active', 'South Korean', '1998-12-14', 26),
(13, 3, 'Zhang Hao', 'Center, Vocalist', 'Active', 'Chinese', '2000-07-25', 25),
(14, 3, 'Sung Han-bin', 'Leader, Vocalist, Dancer', 'Active', 'South Korean', '2001-06-13', 24),
(15, 3, 'Seok Matthew', 'Vocalist', 'Active', 'South Korean / Canadian', '2002-05-28', 23),
(16, 3, 'Kim Tae-rae', 'Vocalist', 'Active', 'South Korean', '2002-07-14', 23),
(17, 3, 'Ricky (Shen Quanrui)', 'Vocalist, Rapper', 'Active', 'Chinese', '2004-05-20', 21),
(18, 3, 'Kim Gyu-vin', 'Vocalist, Rapper', 'Active', 'South Korean', '2004-08-30', 21),
(19, 3, 'Park Gun-wook', 'Rapper, Dancer, Vocalist', 'Active', 'South Korean', '2005-01-10', 20),
(20, 3, 'Han Yu-jin', 'Vocalist, Dancer, Maknae', 'Active', 'South Korean', '2007-03-20', 18),
(21, 4, 'Lee Chan-hyuk', 'Vocalist, Rapper, Producer', 'Active', 'South Korean', '1996-09-12', 29),
(22, 4, 'Lee Su-hyun', 'Vocalist, Maknae', 'Active', 'South Korean', '1999-05-04', 26),
(23, 5, 'Karina (Yu Ji-min)', 'Leader, Dancer, Rapper, Vocalist', 'Active', 'South Korean', '2000-04-11', 25),
(24, 5, 'Giselle (Uchinaga Eri)', 'Rapper, Vocalist', 'Active', 'Japanese / South Korean', '2000-10-30', 25),
(25, 5, 'Winter (Kim Min-jeong)', 'Vocalist, Dancer', 'Active', 'South Korean', '2001-01-01', 24),
(26, 5, 'Ningning (Ning Yizhuo)', 'Vocalist, Maknae', 'Active', 'Chinese', '2002-10-23', 23),
(27, 6, 'Minji (Kim Min-ji)', 'Leader, Vocalist, Dancer', 'Hiatus', 'South Korean', '2004-05-07', 21),
(28, 6, 'Hanni (Pham Ngoc Han)', 'Vocalist, Dancer', 'Hiatus', 'Vietnamese / Australian', '2004-10-06', 21),
(29, 6, 'Danielle (Mo Ji-hye)', 'Vocalist, Dancer', 'Hiatus', 'South Korean / Australian', '2005-04-11', 20),
(30, 6, 'Haerin (Kang Hae-rin)', 'Vocalist, Dancer', 'Hiatus', 'South Korean', '2006-05-15', 19),
(31, 6, 'Hyein (Lee Hye-in)', 'Vocalist, Dancer, Maknae', 'Hiatus', 'South Korean', '2008-04-21', 17),
(32, 7, 'Kwon Eun-bi', 'Leader, Vocalist, Dancer', 'Inactive', 'South Korean', '1995-09-27', 30),
(33, 7, 'Sakura Miyawaki', 'Vocalist, Rapper, Visual', 'Inactive', 'Japanese', '1998-03-19', 27),
(34, 7, 'Kang Hye-won', 'Rapper, Vocalist, Visual', 'Inactive', 'South Korean', '1999-07-05', 26),
(35, 7, 'Choi Ye-na', 'Rapper, Vocalist, Dancer', 'Inactive', 'South Korean', '1999-09-29', 26),
(36, 7, 'Lee Chae-yeon', 'Dancer, Vocalist, Rapper', 'Inactive', 'South Korean', '2000-01-11', 25),
(37, 7, 'Kim Chae-won', 'Vocalist, Dancer', 'Inactive', 'South Korean', '2000-08-01', 25),
(38, 7, 'Kim Min-ju', 'Vocalist, Rapper, Visual', 'Inactive', 'South Korean', '2001-02-05', 24),
(39, 7, 'Nako Yabuki', 'Vocalist', 'Inactive', 'Japanese', '2001-06-18', 24),
(40, 7, 'Hitomi Honda', 'Dancer, Vocalist', 'Inactive', 'Japanese', '2001-10-06', 24),
(41, 7, 'Jo Yu-ri', 'Vocalist', 'Inactive', 'South Korean', '2001-10-22', 24),
(42, 7, 'An Yu-jin', 'Vocalist, Dancer', 'Inactive', 'South Korean', '2003-09-01', 22),
(43, 7, 'Jang Won-young', 'Center, Vocalist, Maknae', 'Inactive', 'South Korean', '2004-08-31', 21);

-- 4. ARTIST_EVENT TABLE (Junction, references Artist and Event)
-- NOTE: Assuming 'Event' records are already inserted or the table is not required to be inserted first.
INSERT INTO Artist_Event (Artist_ID, Event_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(5, 5);

-- 5. ARTIST_FOLLOWER TABLE (Junction, references Artist and Fan)
-- NOTE: Assuming 'Fan' records are already inserted or the table is not required to be inserted first.
INSERT INTO Artist_Follower (Artist_ID, Fan_ID) VALUES
(5, 1),
(7, 1),
(6, 2);

-- 6. SETLIST TABLE (Junction, references Artist and Event)
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