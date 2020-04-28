#login
SELECT ID, password FROM user 
WHERE ID=VARid and password=VARpassword;

#register
INSERT INTO user
SELECT * FROM (SELECT 
VARid,
VARfname,
VARminit,
VARlname,
VARpassword,
VARemail) as temp
WHERE NOT EXISTS (SELECT ID 
				FROM user
				WHERE user.ID = VARuser)
LIMIT 1;



#leavereview
INSERT INTO review
VALUES(
VARpassenger_id, 
VARrid, 
VARshopping, 
VARconnection_speed, 
VARcomment, 
VARapprover_id, 
VARapproval_status, 
VARedit_timestamp,
VARstation_name);

#viewreview
SELECT * FROM review 
ORDER BY passenger_ID ASC;

SELECT * FROM review 
ORDER BY passenger_ID DESC;

SELECT * FROM review 
ORDER BY station_name ASC;

SELECT * FROM review 
ORDER BY station_name DESC;

SELECT * FROM review 
ORDER BY shopping ASC;

SELECT * FROM review 
ORDER BY shopping DESC;

SELECT * FROM review 
ORDER BY connection_speed ASC;

SELECT * FROM review 
ORDER BY connection_speed DESC;

SELECT * FROM review 
ORDER BY approval_status ASC;

SELECT * FROM review 
ORDER BY approval_status DESC;


#editreview
SELECT *
FROM review
WHERE review.rid = VARrid;

UPDATE review
SET shopping=VARshopping, connection_speed=VARspeed, 
comment=VARcomment, 
edit_timestamp=VARtimestamp
WHERE review.rid = VARrid AND passenger_ID = VARid;

DELETE FROM review WHERE rid=VARrid AND passenger_ID=VARpid;


#stationinfo
SELECT * FROM station;

SELECT AVG(shopping)
FROM review;
SELECT AVG(connection_speed)
FROM review;

SELECT first_name, last_name 
FROM user
WHERE ID=review.passenger_ID and approval_status="Approved";

SELECT shopping, connection_speed, comment
FROM review
WHERE approval_status="Approved";

#linesummary
SELECT * FROM station_on_line
WHERE line_name=line.name
ORDER BY order_number DESC;
SELECT * FROM station_on_line
WHERE line_name=line.name
ORDER BY order_number ASC;
SELECT * FROM station_on_line
WHERE line_name=line.name
ORDER BY station_name DESC;
SELECT * FROM station_on_line
WHERE line_name=line.name
ORDER BY station_name ASC;

SELECT COUNT(station_on_line)
WHERE line_name=line.name;

#editprofile
UPDATE users
SET 
ID = newID,
Fname = newfname,
Minit = newminit,
Lname = newlname,
Password = newpassword,
passengeremail = newemail
WHERE NOT EXISTS (SELECT ID
			FROM users);

#buycard
INSERT INTO card
VALUES(
userID, 
"T-mes",
purchasedate, 
Null,
DATE_ADD(purchasedate, INTERVAL 1 MONTH)
);
INSERT INTO card
VALUES(
userID, 
"T-10",
purchasedate, 
10,
Null
);
INSERT INTO card
VALUES(
userID, 
"T-50/30",
purchasedate, 
50,
DATE_ADD(purchasedate, INTERVAL 30 DAY)
);
INSERT INTO card
VALUES(
userID, 
"T-jove",
purchasedate, 
null,
DATE_ADD(purchasedate, INTERVAL 90 DAY)
);

#viewtrips
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY start_date_time ASC;
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY start_date_time DESC;
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY from_station_name ASC;
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY from_station_name DESC;
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY to_station_name ASC;
SELECT start_date_time, end_date_time, card_type, from_station_name, to_station_name
FROM trip
ORDER BY to_station_name DESC;

#updatetrip
UPDATE trip
SET end_date_time = newenddate, 
to_station_name = newstationname
WHERE card.user_ID = userID
AND trip.start_date_time = startdatetime;

#pendingreviews
SELECT first_name, last_name FROM user
WHERE ID= review.passenger_ID;
SELECT station_name, shopping, connection_speed, comment
FROM review
WHERE approval_status= "Pending";
UPDATE review
SET approval_status= "Approved";
UPDATE review
SET approval_status= "Rejected";

#editadminprofile
UPDATE users
SET 
ID = newID,
Fname = newfname,
Minit = newminit,
Lname = newlname,
Password = newpassword
WHERE NOT EXISTS (SELECT ID
			FROM users
            );
DELETE FROM user 
WHERE ID=admin.ID;

#addstation **SKIPPED RN
INSERT INTO station (
Name, 
Status,
State_province,
Address,
Zipcode,
city)
SELECT  (
Name, 
Status,
State_province,
Address,
Zipcode,
city)
WHERE NOT EXISTS (SELECT name
				FROM station
				WHERE name = station.station_name);

INSERT INTO station_on_line (
Station_name,
Line_name,
order_number)
SELECT (
Station_name,
Line_name,
order_number) 
WHERE NOT EXISTS (SELECT name
				FROM station
				WHERE name = station.station_name)
AND NOT EXISTS (SELECT order_number
				FROM station_on_line
		WHERE orderNumber= station_on_line.order_number) ;

INSERT INTO admin_add_station (
Station_name,
admin_ID,
date_time)
SELECT (
Station_name,
admin_ID,
date_time)
WHERE NOT EXISTS (SELECT name
				FROM station
				WHERE name = station.station_name);


#linesummary
SELECT station_name, order_number FROM station_on_line
WHERE line_name=VARname
ORDER BY order_number DESC;

SELECT station_name, order_number FROM station_on_line
WHERE line_name=VARname
ORDER BY order_number ASC;

SELECT station_name, order_number FROM station_on_line
WHERE line_name=VARname
ORDER BY station_on_line DESC;

SELECT station_name, order_number FROM station_on_line
WHERE line_name=VARname
ORDER BY station_on_line ASC;

SELECT COUNT(station_name) FROM station_on_line
WHERE line_name=VARline;

DELETE FROM station_on_line
WHERE station_name=VARstation;	

UPDATE station_on_line
SET order_number=VARnum
WHERE station_name=VARstation;


#stationinfo
SELECT *
FROM station
WHERE name = VARname;

UPDATE station
SET status = VARstatus
WHERE name = VARname;

SELECT AVG(shopping)
FROM review 
WHERE (SELECT shopping
	FROM review
	WHERE station_name = VARstation);

SELECT AVG(connection_speed)
FROM review 
WHERE (SELECT connection_speed
	FROM review
	WHERE station_name = VARstation);






