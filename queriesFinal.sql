#login
SELECT * FROM tmb.user WHERE ID=userID and password=userPassword;

SELECT * FROM tmb.admin WHERE ID=userID;

#register
SELECT ID FROM tmb.user;

INSERT INTO tmb.user (ID, first_name, minit, last_name, password, passenger_email) VALUES (userID, firstName, middleInitial, lastName, password, email);

#leavereview
SELECT * FROM tmb.station ORDER BY name ASC;

SELECT MAX(rID) FROM tmb.review;

INSERT INTO tmb.review (passenger_id, rID, shopping, connection_speed, comment, approver_ID, approval_status, edit_timestamp, station_name) VALUES(userID, reviewID, shopping, connectionSpeed, comment, "pending", selectedStation);


#viewreviews
SELECT * FROM tmb.review WHERE passenger_ID=userID;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY rid ASC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY station_name ASC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY shopping ASC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY connection_speed ASC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY approval_status ASC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY rid DESC

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY station_name DESC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY shopping DESC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY connection_speed DESC;

SELECT * FROM tmb.review WHERE passenger_ID=userID ORDER BY approval_status DESC;



#editreview
SELECT * FROM tmb.review WHERE rid=selected_review;

DELETE FROM tmb.review WHERE rid=selected_review AND passenger_ID=passID;

SELECT * FROM tmb.review WHERE passenger_ID=passID;



#stationinfo
SELECT * FROM tmb.station WHERE name=selectedStation;

SELECT AVG(shopping) FROM review WHERE station_name=selectedStation;

SELECT AVG(connection_speed) FROM review WHERE station_name=selectedStation;

SELECT line_name FROM tmb.station_on_line WHERE station_name=selectedStation;

SELECT passenger_id, shopping, connection_speed, comment FROM tmb.review WHERE station_name=selectedStation;


#linesummary
SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=selectedLine;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY order_number;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY station_name ASC;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY order_number ASC;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY station_name DESC;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY order_number DESC;


#viewtrips
SELECT * FROM tmb.trip WHERE user_ID=userID;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY start_date_time ASC;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY from_station_name ASC;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY to_station_name ASC;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY start_date_time DESC;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY from_station_name DESC;

SELECT * FROM tmb.trip WHERE user_ID=userID ORDER BY to_station_name DESC;



#editProfilePassenger
SELECT * FROM tmb.user WHERE ID=userID;

DELETE FROM tmb.user WHERE ID=userID;
SELECT ID FROM tmb.user;

UPDATE user SET ID = userID, first_name = firstName, minit= middleInitial, last_name= lastName, password= password, passenger_email= email WHERE ID = oldUserID;




#buycard
INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(userID, 'T-mes', NOW(), NULL, DATE_ADD(CURDATE(), INTERVAL 1 MONTH));

INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(userID, ‘T-10’, NOW(), 10, NULL);

INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(userID, ‘T-50/30’, NOW(), 50, DATE_ADD(CURDATE(), INTERVAL 30 DAY));

INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(userID, ‘T-jove’, NOW(), NULL, DATE_ADD(CURDATE(), INTERVAL 90 DAY));



#goOnatrip
SELECT name FROM tmb.station ORDER BY name ASC;

SELECT type, purchase_date_time FROM tmb.card WHERE (uses_left > 0 or uses_left IS NULL) AND user_ID = userID AND  (CURDATE() <= expiration_date or expiration_date IS NULL);

SELECT type, purchase_date_time FROM tmb.card WHERE (uses_left > 0 or uses_left IS NULL) AND user_ID = userID AND  CURDATE() <= expiration_date;

INSERT INTO tmb.trip (user_ID, card_type, card_purchase_date_time, start_date_time, end_date_time, from_station_name, to_station_name) VALUES (userID, cardUsed, purchase_date_time, NOW(), NULL, startSation, NULL);

UPDATE card SET uses_left = uses_left - 1 WHERE user_ID = userID;

#updatetrip
SELECT from_station_name, card_type, card_purchase_date_time, start_date_time FROM tmb.trip WHERE start_date_time=start_date_time;

SELECT name FROM tmb.station;

SELECT * FROM tmb.trip WHERE user_ID=userID;

SELECT from_station_name, card_type, card_purchase_date_time FROM tmb.trip WHERE start_date_time=start_date_time;

UPDATE tmb.trip SET end_date_time=NOW(), to_station_name=stationName WHERE card_type=cardType AND card_purchase_date_time=cardPurchase AND from_station_name=stationName;


#editprofileadmin
SELECT * FROM tmb.user WHERE ID=userID;

SELECT station_name FROM tmb.admin_add_station WHERE admin_ID=userID;

DELETE FROM tmb.station WHERE station_name=stationToDelete;

SELECT line_name FROM tmb.admin_add_line WHERE admin_ID=userUD;

DELETE FROM tmb.line WHERE name=lineToDelete;

DELETE FROM tmb.user WHERE ID=userID;

SELECT ID FROM tmb.user;

UPDATE user SET ID = userID, first_name = firstName, minit= middleInitial, last_name= lastName, password= password WHERE ID = oldUserId;


#addstation
SELECT name FROM tmb.line;

SELECT line_name, order_number FROM tmb.station_on_line;

INSERT INTO tmb.station (name, status, state_province, address, zipcode, city) VALUES (stationName,“open”, state, address, zip, city);

INSERT INTO tmb.station_on_line (station_name, line_name, order_number) VALUES (stationName,line, ordernum);

#addline
SELECT name FROM tmb.station ORDER BY name ASC;

INSERT INTO tmb.line (name) VALUES (lineNname);

INSERT INTO tmb.station_on_line (station_name, line_name, order_number) VALUES (stationOrder, lineName, stationOrder);

INSERT INTO tmb.admin_add_station (station_name, admin_ID, date_time) VALUES (stationName, userID, NOW());

INSERT INTO tmb.admin_add_line (line_name, admin_ID, date_time) VALUES (lineName, userID, NOW());


#reviewpassengerreviews
SELECT tmb.user.first_name, tmb.user.last_name, tmb.review.station_name, tmb.review.shopping, tmb.review.connection_speed, tmb.review.comment, tmb.review.rID, tmb.user.ID FROM user JOIN review ON tmb.user.ID=tmb.review.passenger_ID WHERE tmb.review.approval_status='pending';


UPDATE tmb.review SET approval_status= 'approved' WHERE rID=rID AND passenger_ID=userID;

UPDATE tmb.review SET approval_status= 'rejected' WHERE rID=rID AND passenger_ID=userID;




#stationInfoAdmin
SELECT * FROM tmb.station WHERE name=selectedStation;

SELECT AVG(shopping) FROM review WHERE station_name=selectedStation;

SELECT AVG(connection_speed) FROM review WHERE station_name=selectedStation;

SELECT line_name FROM tmb.station_on_line WHERE station_name=selectedStation;

SELECT passenger_id, shopping, connection_speed, comment FROM tmb.review WHERE station_name=selectedStation;

UPDATE station SET status = stationStatus WHERE name = selectedStation;

#lineSummaryAdmin
SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=selectedLine;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY station_name DESC;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY station_name ASC;

DELETE FROM tmb.station WHERE name=stationName;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY order_number ASC;

SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=selectedLine ORDER BY order_number DESC;









