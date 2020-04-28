from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import Flask, flash, redirect, render_template, request, session, abort
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'roman64'
app.config['MYSQL_DB'] = 'tmb'


app.secret_key = "super secret key"

mysql = MySQL(app)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form['userID']
        userPassword = request.form['password'].encode('utf-8')

        if userID is "" or userPassword is "":
            return "Invalid login credentials. Click back to return to login screen."

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.user WHERE ID=%s and password=%s", (userID, userPassword))
        user = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.admin WHERE ID=%s", [userID])
        admin = cur.fetchone()
        cur.close()

        if user == None:
            return "Invalid login credentials. Click back to return to login screen."
        else:
            session['name'] = user[1]
            session['lastName'] = user[3]
            session['userID'] = user[0]
            try:
                user[0] == admin[0]
                session['type'] = 'admin'
                return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])
            except:
                session['type'] = 'passenger'
                return render_template("passengerLanding.html", firstName=user[1], lastName=user[3])

    else:
        return render_template("login.html")

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        firstName = request.form['firstName']
        middleInitial = request.form['middleInitial']
        lastName = request.form['lastName']
        email = request.form['email']
        userID = request.form['userID']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        cur = mysql.connection.cursor()
        cur.execute("SELECT ID FROM tmb.user")
        userIDs = cur.fetchall()
        cur.close()

        if (firstName is "" or lastName is "" or email is "" or userID is "" or password is "" or confirmPassword is ""):
            return "Please fill out all the required fields (everything except middle initial)"

        userIDTuple = userID,
        for username in userIDs:
            if userIDTuple == username:
                return "Sorry that userID is already taken"

        if (password != confirmPassword):
            return "The two passwords do not match"

        if len(password) < 8:
            return "The password must be at least 8 characters"


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tmb.user (ID, first_name, minit, last_name, password, passenger_email) VALUES (%s, %s, %s, %s, %s, %s)", (userID, firstName, middleInitial, lastName, password, email))
        mysql.connection.commit()

        session['userID'] = userID
        session['name'] = firstName
        session['lastName'] = lastName
        session['type'] = 'passenger'
        return render_template("passengerLanding.html", firstName=firstName, lastName=lastName)



@app.route('/passengerLanding', methods=['GET'])
def passengerLanding():
    if request.method == "GET":
        first = session['name']
        last = session['lastName']
        return render_template("passengerLanding.html", firstName=first, lastName=last)


@app.route('/leaveReview', methods=['GET', 'POST'])
def leaveReview():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.station ORDER BY name ASC")
        stations = cur.fetchall()
        cur.close()

        stationList = []
        for stationTuple in stations:
            stationList.append(stationTuple[0])
        stationList = [str(i) for i in stationList]
        return render_template('leaveReview.html', option_list = stationList)
    else:
        selectedStation = request.form['stationSelect']
        shopping = request.form.get('shopping', type=int)
        connectionSpeed = request.form.get('connectionSpeed', type=int)
        comment = request.form['comment']

        if selectedStation == "none" or shopping == "" or connectionSpeed == "":
            return "Make sure to select a station, shopping rating, and connection speed rating"

        cur = mysql.connection.cursor()
        cur.execute("SELECT MAX(rID) FROM tmb.review")
        reviewID = cur.fetchall()
        reviewID = reviewID[0][0] + 1

        cur.execute("INSERT INTO tmb.review (passenger_id, rID, shopping, connection_speed, comment, approver_ID, approval_status, edit_timestamp, station_name) VALUES (%s, %s, %s, %s, %s, NULL, %s, NOW(), %s)", (session['userID'], reviewID, shopping, connectionSpeed, comment, "pending", selectedStation))
        mysql.connection.commit()

        return render_template("passengerLanding.html", firstName=session['name'], lastName=session['lastName'])



@app.route('/viewReviews', methods=['GET', 'POST'])
def viewReviews():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)


@app.route('/viewReviewsSortedByIdAsc', methods=['GET'])
def viewReviewsSortedByIdAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY rid ASC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)


@app.route('/viewReviewsSortedByStationAsc', methods=['GET'])
def viewReviewsSortedByStationAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY station_name ASC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByShoppingAsc', methods=['GET'])
def viewReviewsSortedByShoppingAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY shopping ASC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByConnectionSpeedAsc', methods=['GET'])
def viewReviewsSortedByConnectionSpeedAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY connection_speed ASC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByApprovalStatusAsc', methods=['GET'])
def viewReviewsSortedByApprovalStatusAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY approval_status ASC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)


@app.route('/viewReviewsSortedByIdDesc', methods=['GET'])
def viewReviewsSortedByIdDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY rid DESC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)


@app.route('/viewReviewsSortedByStationDesc', methods=['GET'])
def viewReviewsSortedByStationDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY station_name DESC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByShoppingDesc', methods=['GET'])
def viewReviewsSortedByShoppingDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY shopping DESC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByConnectionSpeedDesc', methods=['GET'])
def viewReviewsSortedByConnectionSpeedDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY connection_speed DESC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)

@app.route('/viewReviewsSortedByApprovalStatusDesc', methods=['GET'])
def viewReviewsSortedByApprovalStatusDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s ORDER BY approval_status DESC", (userID,))
    reviews = cur.fetchall()
    cur.close()
    return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)


@app.route('/editReview', methods=['GET', 'POST'])
def editReview():
    selected_review = request.args.get('type')

    if request.method== 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.review WHERE rid=%s", (selected_review,))
        review = cur.fetchone()
        cur.close()

        return render_template("editReview.html", stationName=review[8], status=review[6], rid=review[1], shopping=review[2], connectionSpeed=review[3], comment=review[4])
    else:
        if request.form["button"] == "Delete Review":
            return url
            passID = session['userID']
            cur = mysql.connection.cursor()
            numdelete = cur.execute("DELETE FROM tmb.review WHERE rid=%s AND passenger_ID=%s", (selected_review, passID))
            mysql.connection.commit()


            cur.execute("SELECT * FROM tmb.review WHERE passenger_ID=%s", (passID,))
            reviews = cur.fetchall()

            cur.close()

            return render_template("viewReviews.html", firstName= session['name'], lastName= session['lastName'], rows=reviews)


@app.route('/stationInfo<selectedStation>', methods=['GET', 'POST'])
def stationInfo(selectedStation):
    if selectedStation == "None":
        return "This destination does not exist"
    if request.method== 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.station WHERE name=%s", (selectedStation,))
        station = cur.fetchone()

        cur.execute("SELECT AVG(shopping) FROM review WHERE station_name=%s", (selectedStation,))
        try:
            avgShopping = int(cur.fetchone()[0])
        except:
            avgShopping = 0

        cur.execute("SELECT AVG(connection_speed) FROM review WHERE station_name=%s", (selectedStation,))

        try:
            avgConSpeed = int(cur.fetchone()[0])
        except:
            avgConSpeed = 0

        cur.execute("SELECT line_name FROM tmb.station_on_line WHERE station_name=%s", (selectedStation,))
        lines = cur.fetchall()

        lineList = []
        for lineTup in lines:
            lineList.append(lineTup[0])

        cur.execute("SELECT passenger_id, shopping, connection_speed, comment FROM tmb.review WHERE station_name=%s", (selectedStation,))
        reviews = cur.fetchall()

        cur.close()


    return render_template("stationInfo.html", rows=reviews, station=station[0], status=station[1], address=station[3], shopping=avgShopping, connectionSpeed=avgConSpeed, lines=lineList)


@app.route('/lineSummary<line>', methods=['GET', 'POST'])
def lineSummary(line):
    if request.method == "GET":
        selectedLine = line
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY order_number", (selectedLine,))
        stations = cur.fetchall()

        return render_template("lineSummary.html", lineName=selectedLine, numberStops=numStops, stations=stations)

    if request.method == "POST":
        lineSelected = request.form['update']
        return lineSelected


@app.route('/lineSummarySortedByStationAsc<line>', methods=['GET', 'POST'])
def lineSummarySortedByStationAsc(line):
    if request.method == "GET":
        selectedLine = line
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY station_name ASC", (selectedLine,))
        stations = cur.fetchall()

        return render_template("lineSummary.html", lineName=selectedLine, numberStops=numStops, stations=stations)
    else:
        return 'yo'


@app.route('/lineSummarySortedByOrderAsc<line>', methods=['GET', 'POST'])
def lineSummarySortedByOrderAsc(line):
    if request.method == "GET":
        selectedLine = line

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY order_number ASC", (selectedLine,))
        stations = cur.fetchall()

        return render_template("lineSummary.html", lineName=selectedLine, numberStops=numStops, stations=stations)
    else:
        return 'yo'

@app.route('/lineSummarySortedByStationDesc<line>', methods=['GET', 'POST'])
def lineSummarySortedByStationDesc(line):
    if request.method == "GET":
        selectedLine = line
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY station_name DESC", (selectedLine,))
        stations = cur.fetchall()

        return render_template("lineSummary.html", lineName=selectedLine, numberStops=numStops, stations=stations)
    else:
        return 'yo'


@app.route('/lineSummarySortedByOrderDesc<line>', methods=['GET', 'POST'])
def lineSummarySortedByOrderDesc(line):
    if request.method == "GET":
        selectedLine = line

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY order_number DESC", (selectedLine,))
        stations = cur.fetchall()

        return render_template("lineSummary.html", lineName=selectedLine, numberStops=numStops, stations=stations)
    else:
        return 'yo'


#ALL VIEW TRIPS STUFF
@app.route('/viewTrips', methods=['GET', 'POST'])
def viewTrips():
    if request.method == "GET":
        userID = session['userID']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s", (userID,))
        trips = cur.fetchall()
        cur.close()

        if session['type'] == 'admin':
            var = 'Admin'
        else:
            var = ''
        return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips, session=var)
    else:
        return "yooo"

@app.route('/viewTripsSortedByStartDateTimeAsc', methods=['GET'])
def viewTripsSortedByStartDateTimeAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY start_date_time ASC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)

@app.route('/viewTripsSortedByFromStationAsc', methods=['GET'])
def viewTripsSortedByFromStationAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY from_station_name ASC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)


@app.route('/viewTripsSortedByToStationAsc', methods=['GET'])
def viewTripsSortedByToStationAsc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY to_station_name ASC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)


@app.route('/viewTripsSortedByStartDateTimeDesc', methods=['GET'])
def viewTripsSortedByStartDateTimeDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY start_date_time DESC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)

@app.route('/viewTripsSortedByFromStationDesc', methods=['GET'])
def viewTripsSortedByFromStationDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY from_station_name DESC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)


@app.route('/viewTripsSortedByToStationDesc', methods=['GET'])
def viewTripsSortedByToStationDesc():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s ORDER BY to_station_name DESC", (userID,))
    trips = cur.fetchall()
    cur.close()
    return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)


@app.route('/editProfilePassenger', methods=['GET', 'POST'])
def editProfilePassenger():
    if request.method == "GET":
        userID = session['userID']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.user WHERE ID=%s", (userID,))
        user = cur.fetchone()
        cur.close()

        middleI = user[2]
        if middleI == "":
            middleI = "n/a"
        return render_template("editProfilePassenger.html", firstName= user[1], middleInitial=middleI, lastName= user[3],
            email=user[5], password=user[4], user=user[0])
    else:
        if request.form["action"] == "Delete":
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM tmb.user WHERE ID=%s", (session['userID'],))
            mysql.connection.commit()
            cur.close()
            return render_template("login.html")
        elif request.form['action'] == "Update":
            firstName = request.form['firstName']
            middleInitial = request.form['middleInitial']
            if middleInitial == "n/a":
                middleInitial = ""
            lastName = request.form['lastName']
            email = request.form['email']
            userID = request.form['userID']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            oldUserID = session['userID']

            cur = mysql.connection.cursor()
            cur.execute("SELECT ID FROM tmb.user")
            userIDs = cur.fetchall()
            cur.close()

            if (firstName is "" or lastName is "" or email is "" or userID is "" or password is "" or confirmPassword is ""):
                return "Please fill out all the required fields (everything except middle initial)"

            # userIDTuple = userID
            # for username in userIDs:
            #     if  oldUserID != username and userIDTuple == username:
            #             return "Sorry that userID is already taken"

            if (password != confirmPassword):
                return "The two passwords do not match"

            if len(password) < 8:
                return "The password must be at least 8 characters long"

            cur = mysql.connection.cursor()
            try:
                cur.execute("UPDATE user SET ID = %s, first_name = %s, minit= %s, last_name= %s, password= %s, passenger_email= %s WHERE ID = %s",
                    (userID, firstName, middleInitial, lastName, password, email, oldUserID))
                mysql.connection.commit()
            except:
                return "User input is invalid"
            session['name'] = firstName
            session['lastName'] = lastName

            return render_template("passengerLanding.html", firstName=session['name'], lastName=session['lastName'])



@app.route('/buyCard', methods=['GET', 'POST'])
def buyCard():
    if request.method == "GET":
        return render_template("buyCard.html")
    else:
        cur = mysql.connection.cursor()


        if request.form["cardType"] == "T-mes":
            session['card'] = "T-mes"
            cur.execute("INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(%s, %s, NOW(), NULL, DATE_ADD(CURDATE(), INTERVAL 1 MONTH))", (session['userID'], 'T-mes'))
        elif request.form["cardType"] == "T-10":
            session['card'] = "T-10"
            cur.execute("INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(%s, %s, NOW(), 10, NULL)", (session['userID'], 'T-10'))
        elif request.form["cardType"] == "T-50/30":
            session['card'] = "T-50/30"
            cur.execute("INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(%s, %s, NOW(), 50, DATE_ADD(CURDATE(), INTERVAL 30 DAY))", (session['userID'], 'T-50/30'))
        elif request.form["cardType"] == "T-jove":
            session['card'] = "T-jove"
            cur.execute("INSERT INTO tmb.card (user_ID, type, purchase_date_time, uses_left, expiration_date) VALUES(%s, %s, NOW(), NULL, DATE_ADD(CURDATE(), INTERVAL 90 DAY))", (session['userID'], 'T-jove'))

        mysql.connection.commit()
        if session['type'] == 'admin':
            return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])
        else:
            return render_template("passengerLanding.html", firstName=session['name'], lastName=session['lastName'])


@app.route('/goOnATrip', methods=['GET', 'POST'])
def goOnATrip():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM tmb.station ORDER BY name ASC")
        stations = cur.fetchall()

        stationList = []
        for stationTuple in stations:
            stationList.append(stationTuple[0])
        stationList = [str(i) for i in stationList]

        cur.execute("SELECT type, purchase_date_time FROM tmb.card WHERE (uses_left > 0 or uses_left IS NULL) AND user_ID = %s AND  (CURDATE() <= expiration_date or expiration_date IS NULL)", (session['userID'],))
        cardData = cur.fetchall()

        cur.close()
        return render_template("goOnATrip.html", stations=stationList, cards=cardData)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT type, purchase_date_time FROM tmb.card WHERE (uses_left > 0 or uses_left IS NULL) AND user_ID = %s AND  CURDATE() <= expiration_date", (session['userID'],))
        rowCount = cur.rowcount
        if rowCount == 0:
            return "You don't have any cards"
        else:
            startStation = request.form['startStation']
            cardData = request.form['cardUsed']
            ind = cardData.find(" ")
            cardUsed = cardData[:ind]
            purchase_date_time = cardData[ind+1:]

            cur.execute("INSERT INTO tmb.trip (user_ID, card_type, card_purchase_date_time, start_date_time, end_date_time, from_station_name, to_station_name) VALUES (%s, %s, %s, NOW(), NULL, %s, NULL)", (session['userID'], cardUsed, purchase_date_time, startStation))
            mysql.connection.commit()

            cur.execute("UPDATE card SET uses_left = uses_left - 1 WHERE user_ID = %s", (session['userID'],))
            mysql.connection.commit()
            if session['type'] == 'admin':
                return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])
            else:
                return render_template("passengerLanding.html", firstName=session['name'], lastName=session['lastName'])


@app.route('/updateTrip<start_date_time>', methods=['GET', "POST"])
def updateTrip(start_date_time):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT from_station_name, card_type, card_purchase_date_time, start_date_time FROM tmb.trip WHERE start_date_time=%s", (start_date_time,))
        tripData = cur.fetchone()

        cur.execute("SELECT name FROM tmb.station")
        stations = cur.fetchall()

        return render_template("updateTrip.html", tripData=tripData, stations=stations)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s", (session['userID'],))
        trips = cur.fetchall()

        cur.execute("SELECT from_station_name, card_type, card_purchase_date_time FROM tmb.trip WHERE start_date_time=%s", (start_date_time,))
        tripData = cur.fetchone()

        endStation = request.form['endStation']

        cur.execute("UPDATE tmb.trip SET end_date_time=NOW(), to_station_name=%s WHERE card_type=%s AND card_purchase_date_time=%s AND from_station_name=%s", (endStation, tripData[1], tripData[2], tripData[0]))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.trip WHERE user_ID=%s", (session['userID'],))
        trips = cur.fetchall()

        cur.close()
        return render_template("viewTrips.html", firstName= session['name'], lastName= session['lastName'], rows= trips)


@app.route('/adminLanding', methods=['GET'])
def adminLanding():
    if request.method == "GET":
        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])



#added by Saachi

@app.route('/editProfileAdmin', methods=['GET', 'POST'])
def editProfileAdmin():
    if request.method == "GET":
        userID = session['userID']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.user WHERE ID=%s", (userID,))
        user = cur.fetchone()
        cur.close()

        middleI = user[2]
        if middleI == "" or middleI is None:
            middleI = "n/a"
        return render_template("editProfileAdmin.html", firstName= user[1], middleInitial=middleI, lastName= user[3],
            email=user[5], password=user[4], user=user[0])
    else:
        if request.form["action"] == "Delete":
            cur = mysql.connection.cursor()

            cur.execute("SELECT station_name FROM tmb.admin_add_station WHERE admin_ID=%s", (session["userID"],))
            stationsToDelete = cur.fetchall()
            for stationToDelete in stationsToDelete:
                cur.execute("DELETE FROM tmb.station WHERE station_name=%s", (stationToDelete,))

            cur.execute("SELECT line_name FROM tmb.admin_add_line WHERE admin_ID=%s", (session["userID"],))
            linesToDelete = cur.fetchall()
            for lineToDelete in linesToDelete:
                cur.execute("DELETE FROM tmb.line WHERE name=%s", (lineToDelete,))

            cur.execute("DELETE FROM tmb.user WHERE ID=%s", (session['userID'],))
            mysql.connection.commit()
            cur.close()
            return render_template("login.html")
        elif request.form['action'] == "Update":
            firstName = request.form['firstName']
            middleInitial = request.form['middleInitial']
            if middleInitial == "n/a":
                middleInitial = ""
            lastName = request.form['lastName']
            userID = request.form['userID']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            oldUserID = session['userID']

            cur = mysql.connection.cursor()
            cur.execute("SELECT ID FROM tmb.user")
            userIDs = cur.fetchall()
            cur.close()

            if (firstName is "" or lastName is "" or  userID is "" or password is "" or confirmPassword is ""):
                return "Please fill out all the required fields (everything except middle initial)"

            if (password != confirmPassword):
                return "The two passwords do not match"

            if len(password) < 8:
                return "The password must be at least 8 characters long"

            cur = mysql.connection.cursor()
            try:
                cur.execute("UPDATE user SET ID = %s, first_name = %s, minit= %s, last_name= %s, password= %s WHERE ID = %s",
                    (userID, firstName, middleInitial, lastName, password, oldUserID))
                mysql.connection.commit()
            except:
                return "User input is invalid"
            session['name'] = firstName
            session['lastName'] = lastName

            return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])


global lineOrderList
lineOrderList = []
@app.route('/addStation', methods=['GET', 'POST'])
def addStation():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM tmb.line")
    lines = cur.fetchall()
    if request.method == "GET":
        return render_template("addStation.html", lines=lines)
    else:
        if request.form["action"] == "Add Line":
            lineSelected = request.form['line']
            orderInputted = request.form['order']

            tup = (lineSelected, orderInputted)

            lineOrderList.append(tup)
            return render_template("addStation.html", lines=lines, lineSelected=lineSelected, orderInputted=orderInputted, datas=lineOrderList)
        if request.form['action'] == "Add Station":
            stationName = request.form['stationName']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            postal = request.form['postal']

            if lineOrderList == []:
                return "A station must be on a line"

            cur.execute("SELECT line_name, order_number FROM tmb.station_on_line")
            stationLine = cur.fetchall()

            for stationLineCombo in stationLine:
                for lineOrder in lineOrderList:
                    if stationLineCombo[0] == lineOrder[0] and str(stationLineCombo[1]) == str(lineOrder[1]):
                        return "Invalid order number inputted"

            try:
                cur.execute("INSERT INTO tmb.station (name, status, state_province, address, zipcode, city) VALUES (%s, %s, %s, %s, %s, %s)", (stationName, "open", state, address, postal, city))
                for lineOrder in lineOrderList:
                    cur.execute("INSERT INTO tmb.station_on_line (station_name, line_name, order_number) VALUES (%s, %s, %s)", (stationName, lineOrder[0], lineOrder[1]))

                cur.execute("INSERT INTO tmb.admin_add_station (station_name, admin_ID, date_time) VALUES (%s, %s, NOW())", (stationName, session["userID"]))
                # lineOrderList = []
            except:
                return "An error occurred, and the station could not be added"

            lineOrder = []
            mysql.connection.commit()
        cur.close()
        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])


global stationOrder
stationOrderList = []
@app.route('/addLine', methods=['GET', 'POST'])
def addLine():
    userID = session['userID']
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM tmb.station ORDER BY name ASC")
    stationList = cur.fetchall()
    if request.method == "GET":
        return render_template("addLine.html", stations = stationList)
    else:
        if request.form["action"] == "Add Station":
            stationName = request.form['stationName']
            orderNumber = request.form['order']

            for stationOrder in stationOrderList:
                if str(stationOrder[1]) == str(orderNumber):
                    return "Two stations cannot have the same order number"

            tup = (stationName, orderNumber)
            stationOrderList.append(tup)
            return render_template("addLine.html", stations=stationList, datas=stationOrderList)
        if request.form["action"] == "Add Line":
            lineName = request.form['lineName']

            try:
                cur.execute("INSERT INTO tmb.line (name) VALUES (%s)", [lineName])
                for stationOrder in stationOrderList:
                    cur.execute("INSERT INTO tmb.station_on_line (station_name, line_name, order_number) VALUES (%s, %s, %s)", (stationOrder[0], lineName, stationOrder[1]))

                cur.execute("INSERT INTO tmb.admin_add_line (line_name, admin_ID, date_time) VALUES (%s, %s, NOW())", (lineName, session["userID"]))

            except:
                return "An error occurred while trying to add the line"

            mysql.connection.commit()
        cur.close()
        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])





@app.route('/reviewPassengerReviews', methods=['GET', 'POST'])
def reviewPassengerReviews():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT tmb.user.first_name, tmb.user.last_name, tmb.review.station_name, tmb.review.shopping, tmb.review.connection_speed, tmb.review.comment, tmb.review.rID, tmb.user.ID FROM user JOIN review ON tmb.user.ID=tmb.review.passenger_ID WHERE tmb.review.approval_status='pending'")
        reviews = cur.fetchall()
        return render_template("reviewPassengerReviews.html", firstName= session['name'], lastName= session['lastName'], rows= reviews)
    else:
        if request.form["action"] == "Approve":
            rID= request.form['rid']
            userID=request.form['userid']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE tmb.review SET approval_status= 'approved' WHERE rID=%s AND passenger_ID=%s", (rID, userID))
            mysql.connection.commit()

        elif request.form["action"] == "Reject":
            rID= request.form['rid']
            userID=request.form['userid']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE tmb.review SET approval_status= 'rejected' WHERE rID=%s AND passenger_ID=%s", (rID, userID))
            mysql.connection.commit()
        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])


@app.route('/stationInfoAdmin<selectedStation>', methods=['GET', 'POST'])
def stationInfoAdmin(selectedStation):
    # selectedStation = request.args.get('type')
    if request.method== 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tmb.station WHERE name=%s", (selectedStation,))
        station = cur.fetchone()


        if station is None:
            return "This destination does not exist"

        cur.execute("SELECT AVG(shopping) FROM review WHERE station_name=%s", (selectedStation,))
        try:
            avgShopping = int(cur.fetchone()[0])
        except:
            avgShopping = 0

        cur.execute("SELECT AVG(connection_speed) FROM review WHERE station_name=%s", (selectedStation,))

        try:
            avgConSpeed = int(cur.fetchone()[0])
        except:
            avgConSpeed = 0

        cur.execute("SELECT line_name FROM tmb.station_on_line WHERE station_name=%s", (selectedStation,))
        lines = cur.fetchall()

        lineList = []
        for lineTup in lines:
            lineList.append(lineTup[0])

        cur.execute("SELECT passenger_id, shopping, connection_speed, comment FROM tmb.review WHERE station_name=%s", (selectedStation,))
        reviews = cur.fetchall()

        cur.close()

        return render_template("stationInfoAdmin.html", rows=reviews, station=station[0], status=station[1], address=station[3], shopping=avgShopping, connectionSpeed=avgConSpeed, lines=lineList)

    else:
        if request.form["button"] == "Save":
            stationStatus = request.form['stationStatus']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE station SET status = %s WHERE name = %s;", (stationStatus, selectedStation))
            mysql.connection.commit()
            #cur.close()

        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])



@app.route('/lineSummaryAdmin<selectedLine>', methods=['GET', 'POST'])
def lineSummaryAdmin(selectedLine):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
    numStops = cur.fetchone()[0]

    cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY station_name DESC", (selectedLine,))
    stationDatas = cur.fetchall()

    if request.method == "POST":
        if request.form["action"] == "Update":
            listOfOrders = []
            for stationData in stationDatas:
                orderNum = request.form[str(stationData[1])]

                listOfOrders.append(orderNum)

            duplicates = False
            seen = set()
            for i in listOfOrders:
                if i in seen:
                    duplicates = True
                seen.add(i)

            if duplicates:
                return "Stations on the same line must have different numbers"
            return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])
        else:
            stationName=request.form["station_name"]
            cur.execute("DELETE FROM tmb.station WHERE name=%s", (stationName,))


            mysql.connection.commit()
            return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])

        return render_template("adminLanding.html", firstName=session['name'], lastName=session['lastName'])

    else:

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]


        return render_template("lineSummaryAdmin.html", line=selectedLine, numStops=numStops, stationDatas=stationDatas)


@app.route('/lineSummaryAdminSortedByStationAsc<selectedLine>', methods=['GET', 'POST'])
def lineSummaryAdminSortedByStationAsc(selectedLine):
    if request.method == "GET":

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY station_name ASC", (selectedLine,))
        stationDatas = cur.fetchall()

        return render_template("lineSummaryAdmin.html", line=selectedLine, numStops=numStops, stationDatas=stationDatas)


@app.route('/lineSummaryAdminSortedByStationDesc<selectedLine>', methods=['GET', 'POST'])
def lineSummaryAdminSortedByStationDesc(selectedLine):
    if request.method == "GET":

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY station_name DESC", (selectedLine,))
        stationDatas = cur.fetchall()

        return render_template("lineSummaryAdmin.html", line=selectedLine, numStops=numStops, stationDatas=stationDatas)


@app.route('/lineSummaryAdminSortedByOrderAsc<selectedLine>', methods=['GET', 'POST'])
def lineSummaryAdminSortedByOrderAsc(selectedLine):
    if request.method == "GET":

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY order_number ASC", (selectedLine,))
        stationDatas = cur.fetchall()

        return render_template("lineSummaryAdmin.html", line=selectedLine, numStops=numStops, stationDatas=stationDatas)


@app.route('/lineSummaryAdminSortedByOrderDesc<selectedLine>', methods=['GET', 'POST'])
def lineSummaryAdminSortedByOrderDesc(selectedLine):
    if request.method == "GET":

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(station_name) FROM tmb.station_on_line WHERE line_name=%s", (selectedLine,))
        numStops = cur.fetchone()[0]

        cur.execute("SELECT station_name, order_number FROM tmb.station_on_line WHERE line_name=%s ORDER BY order_number DESC", (selectedLine,))
        stationDatas = cur.fetchall()

        return render_template("lineSummaryAdmin.html", line=selectedLine, numStops=numStops, stationDatas=stationDatas)

if __name__ == "__main__":
    app.run(debug=True)
