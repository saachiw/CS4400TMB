INSERT INTO Line VALUES('L1');

INSERT INTO User VALUES('chall68',	'Charles',	'J',	'Hall',	'pwd', NULL);
INSERT INTO User VALUES('user',	'u','J',	's',	'pwd', NULL);
INSERT INTO User VALUES('wwhite12',	'Walter',	'H',	'White', 'pass123', NULL);


INSERT INTO Admin VALUES('wwhite12');
INSERT INTO card VALUES ('chall68',	'T-mes',	'2019-06-08 10:27:00',	NULL,	
'2019-07-08 10:27:00');
INSERT INTO Station VALUES('Catalunya',	'open',	'Catalonia',	'08002 Barcelona', '08002', 'Barcelona');

INSERT INTO Trip VALUES ('chall68',	'T-mes',	'2019-06-08 10:27:00','2019-06-08 10:29:00', NULL,	
'Catalunya', NULL);

INSERT INTO Review VALUES ('chall68',	'1',	'3',	'4',	'Cool station. Kinda hot though',	'wwhite12',	'approved',	'2019-06-10 14:23:00',	'Catalunya');
INSERT INTO Review VALUES ('chall68',	'2',	'5',	'5',	'Cool station. Kinda hot though',	'wwhite12',	'approved',	'2019-06-10 14:23:00',	'Catalunya');


INSERT INTO Admin_Add_Line VALUES ('L1', 'wwhite12',	'2019-05-10 08:32:00');
INSERT INTO Admin_Add_Station VALUES ('Catalunya', 'wwhite12',	'2019-05-10 08:34:00');
INSERT INTO Station_On_Line VALUES ('Catalunya', 'L1',	16);