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
        ('AESPA Artist Showcase', 'Concert,Fanmeet,Hi Touch', 2, '2026-12-07', '2026-12-07', '18:30:00', '22:30:00');
        
        
select * FROM event;
