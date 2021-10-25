""" File: app.py / server.py """
"""Main multi-threaded Flask application for the trigger engine.
Run only this script using `python app.py` or `flask run`"""

# Importing framework and libraries
from flask import Flask, render_template, request, redirect, url_for
import threading
from collections import defaultdict
import json
print("Importing database utils...")
import db
import timer
print("Importing email and whatsapp bots...")
import bots.mail
if db.WA_OPTION:
    import bots.whatsapp

# Queue for new notifications to be sent to the employee's portal
print("Creating an empty queue for new notifications...")
queue = defaultdict(lambda: [])

# Wrapper function for thread to notify a user
def notifyThread(email, phone, content, type, eid, sub):
    # Adding notification to the queue with employee_id
    queue[eid].append({
                'type': type,
                'content': content
    })
    print("Notification queued for Employee ID:", eid)
    # Sending mail and optionally, whatsapp notifications
    bots.mail.sendMail(email, sub, content)
    if db.WA_OPTION:
        bots.whatsapp.sendMsg(phone, content)

# Function to create and run a thread to notify a user
def notify(email, phone, content, type, eid, sub=db.SUBJECT):
    if type == "":
        type = "rmd"
    threading.Thread(target=notifyThread,
                    daemon=True,
                    args=(email, phone, content, type, eid, sub)).start()


# Function for a thread to run at the start of every day
def dayThread():
    while True:
        # Pausing thread execution till the start of the day
        timer.startDay()

        # Checking for event based notifications to send on a specific day
        notifications = db.pending(trig="DT")
        for notification in notifications:
            # If there exists some notification(s) with this trigger condition:
            _, dt, mn = notification[4].split()
            dt, mn = int(dt), int(mn)
            date, month = timer.curDate(onlydm=True)
            # Checking if today is the date of sending notifications
            if dt == date and mn == month:
                content = notification[1]
                id = notification[0]
                # Creating threads to send notifications to all users
                users = db.getUsers() # Getting info of all users
                for user in users:
                    email, phone, eid = user[1], user[2], int(user[6])
                    # Threads will be created and started inside this function
                    notify(email, phone, content, "rmd", eid)
                db.delete(id)
        
        # Notification for daily transaction scores
        try:
            # Checking if daily minimum and optimum score is defined by the admin
            notification = db.pending(trig="SD")[0]
        except:
            # If not defined, terminating thread execution for today
            # The thread will pause again till the start of the next day
            timer.sleep(2)
            continue
        # Getting minimum and optimum values defined by the admin
        _, minn, opt = notification[4].split()
        users = db.getUsers() # Getting info of all users
        for user in users:
            email, phone, eid = user[1], user[2], int(user[6])
            score = user[3]
            # Checking his/her score lies in which category and notifying accordignly
            # Threads will be created and started inside notify function
            if score < int(minn):
                notify(email, phone, db.SCORE_DAY_LEV1, 'alr', eid)
            elif score < int(opt):
                notify(email, phone, db.SCORE_DAY_LEV2, 'rmd', eid)
            else:
                notify(email, phone, db.SCORE_DAY_LEV3, 'rwd', eid)
        db.resetScore() # Reseting daily score of all users to 0
        # Just a small timer to make sure the function doesn't run multiple times continuosly
        timer.sleep(2)


# Function for a thread to run at the start of every week
def weekThread():
    while True:
        # Pausing thread execution till the start of the week
        timer.startWeek()
        try:
            # Checking if weekly minimum and optimum score is defined by the admin
            notification = db.pending(trig="SW")[0]
        except:
            # If not defined, terminating thread execution for this week
            # The thread will pause again till the start of the next week
            timer.sleep(2)
            continue
        # Getting minimum and optimum values defined by the admin
        _, minn, opt = notification[4].split()
        for user in db.getUsers(): # Getting info of all users
            email, phone, eid = user[1], user[2], int(user[6])
            score = user[4]
            # Checking his/her score lies in which category and notifying accordignly
            # Threads will be created and started inside notify function
            if score < int(minn):
                notify(email, phone, db.SCORE_WEEK_LEV1, 'alr', eid)
            elif score < int(opt):
                notify(email, phone, db.SCORE_WEEK_LEV2, 'rmd', eid)
            else:
                notify(email, phone, db.SCORE_WEEK_LEV3, 'rwd', eid)
        db.resetScore(week=True) # Reseting weekly score of all users to 0
        # Just a small timer to make sure the function doesn't run multiple times continuosly
        timer.sleep(2)


# Function for a thread to run at the start of every month
def monthThread():
    while True:
        # Pausing thread execution till the start of the month
        timer.startMonth()
        try:
            # Checking if monthly minimum and optimum score is defined by the admin
            notification = db.pending(trig="SM")[0]
        except:
            # If not defined, terminating thread execution for this month
            # The thread will pause again till the start of the next month
            timer.sleep(2)
            continue
        # Getting minimum and optimum values defined by the admin
        _, minn, opt = notification[4].split()
        for user in db.getUsers(): # Getting info of all users
            email, phone, eid = user[1], user[2], int(user[6])
            score = user[5]
            # Checking his/her score lies in which category and notifying accordignly
            # Threads will be created and started inside notify function
            if score < int(minn):
                notify(email, phone, db.SCORE_MONTH_LEV1, 'alr', eid)
            elif score < int(opt):
                notify(email, phone, db.SCORE_MONTH_LEV2, 'rmd', eid)
            else:
                notify(email, phone, db.SCORE_MONTH_LEV3, 'rwd', eid)
        db.resetScore(month=True) # Reseting monthly score of all users to 0
        # Just a small timer to make sure the function doesn't run multiple times continuosly
        timer.sleep(2)



# Creating and starting day, week and month threads
# These will be created and started as soon as the flask server is run
# to run at the start of every day, week and month respectively
print("Starting threads for various triggers...")
threading.Thread(target=dayThread, daemon=True).start()
threading.Thread(target=weekThread, daemon=True).start()
threading.Thread(target=monthThread, daemon=True).start()


# Function to notify an employee about his monthly achievement after getting the data through API
def MonthlyAchievementNotif(eid, percent):
    try:
        # Checking if minimum and optimum monthly achievement is defined by the admin
        notification = db.pending(trig="MA")[0]
    except:
        # If not defined, terminating the function
        return
    # Getting the details of the employee
    user = db.getUsers(eid)[0]
    email, phone = user[1], user[2]
    _, minn, opt = notification[4].split()
    # Checking his/her achievement lies in which category and notifying accordignly
    # A thread will be created and started inside notify function
    if percent < int(minn):
        notify(email, phone, db.ACHIEVE_LEV1, 'alr', eid)
    elif percent < int(opt):
        notify(email, phone, db.ACHIEVE_LEV2, 'rmd', eid)
    else:
        notify(email, phone, db.ACHIEVE_LEV3, 'rwd', eid)


# Wrapper function for a thread to send a particular notification
# at a specific time of a day for single or multiple days
# Alternatively, notify a single employee ny passing employee_id
# instead of all Employees (which is default)
def timeNotif(hr, mn, freq, content, id, type='rmd', eid=False):
    while freq > 0:
        # Pausing thread execution till the given time of the day
        timer.afterTime(hr, mn)
        # If the employee_id is given, notify him/her only
        if eid:
            user = db.getUsers(eid)[0] # Getting details of the employee
            email, phone = user[1], user[2]
            # A thread will be created and started inside this function
            notify(email, phone, content, type, eid)
        # If the employee_id is not given, notify everyone
        else:
            for user in db.getUsers(): # Getting details of employees
                email, phone, eid = user[1], user[2], int(user[6])
                # Threads will be created and started inside this function
                notify(email, phone, content, type, eid)

        # Updating the trigger condition in database 
        # to reduce the number of more days this notification will be sent again
        newTrig = f"TM {hr} {mn} {freq-1}"
        db.changeTrigger(id, newTrig)
        freq -= 1
        # Just a small timer to make sure the function doesn't run multiple times continuosly
        timer.sleep(2)
    
    # Delete the notification from database after 0 days are remaining
    db.delete(id)


# Function to send a notification to one or more group(s) only
def rolesNotif(content, roles, type='rmd'):
    users = db.getUsers() # Getting details of employees
    for user in users:
        if user[0] in roles: # Checking if employee lies in the defined group(s)
            email, phone, eid = user[1], user[2], int(user[6])
            notify(email, phone, content, type, eid)


# Funcion to sent alerts if a trigger on user's inactivity is defined
# Returns a false flag when the thread is terminated
def statusNotif():
    try:
        # Checking if user inactivity trigger is defined by the admin
        notification = db.pending(trig="IA")[0]
    except:
        # If not defined, terminating the function 
        # and returning a flag to check that the thread is not active
        return False
    _, hr, mn, everyday = notification[4].split()
    id = int(notification[0])
    hr, mn, everyday = int(hr), int(mn), bool(int(everyday))
    # Pausing thread execution till the given time of the day
    timer.afterTime(hr, mn)
    for user in db.getUsers(): # Fetching data of users
        activity, eid = int(user[7]), int(user[6])
        # If the user was inactive, sending alert
        if activity == 0:
            email, phone = user[1], user[2]
            notify(email, phone, db.INACTIVE, "alr", eid)
        # Else, resetting activity for the day
        else:
            db.addActivity(eid, reset=True)

    # Continuing the thread if the trigger was defined for everyday
    if everyday:
        # Just a small timer to make sure the function doesn't run multiple times continuosly
        timer.sleep(2)
        return statusNotif()
    db.delete(id)
    # Returning a false flag to check that the thread is not active
    return False

# Wrapper function for a thread to send alerts based on user's inactivity
def statusNotifThread():
    global statusNotifThreadActive
    statusNotifThreadActive = statusNotif()

# Function to notify everyone
def notifyAll(content, type):
    for user in db.getUsers():
        email, phone, eid = user[1], user[2], int(user[6])
        notify(email, phone, content, type, eid)


# Creating and starting threads for all stored time based notifications
# This section will run as soon as the flask server is run
# Checking for time based notifications to send at a specified time
print("Loading previously pending notifications from the database...")
notifications = db.pending(trig="TM")
for notification in notifications:
    _, hr, mn, freq = notification[4].split()
    id = int(notification[0])
    hr, mn, freq = int(hr), int(mn), int(freq)
    content = notification[1]
    type = notification[2]
    grp = notification[3]
    # Checking if the notification is for all employees (created by admin)
    if grp == "ALL":
        eid = False
    # Or for a specific employee (created by the employee himself/herself)
    else:
        eid = int(grp)
    # starting a thread to send notification on the specified time
    # for the specified number of days (or a single day)
    threading.Thread(target=timeNotif,
                    daemon=True,
                    args=(hr, mn, freq, content, id, type, eid)).start()

# Creating and starting a thread to notify based on user's inactivity
statusNotifThreadActive = True
threading.Thread(target=statusNotifThread, daemon=True).start()


print("Starting Flask Server...")

# Main Flask Application
app = Flask(__name__)

ERROR_MSG = """<h1> Something went wrong </h1>
            <h3> Please Go back and enter all values in correct format </h3>"""

# Home Route
@app.route('/', methods=['GET', 'POST'])
def index():
    # If signup data is sent via post from /signup
    if request.method == 'POST':
        try:
            # Taking all values from the HTML form
            values = {
                'name': request.form['name'],
                'eid': int(request.form['eid']),
                'sex': request.form['sex'],
                'age': int(request.form['age']),
                'email': request.form['email'],
                'phone': request.form['phone'],
                'grp': request.form['group']
            }
            db.newUser(values) # Registering new user
            return render_template("index.html", reg="User Added")
        except:
            return render_template("signup.html", var="Please Provide Correct Details")
    return render_template("index.html")

# Signup Form
@app.route('/signup')
def signup():
    return render_template("signup.html")

# Route to listen to for Server Sent Events
@app.route('/listen/<int:eid>')
def listen(eid):
    notifications = queue[eid]
    # Checking if there is any new notification in the queue
    if notifications:
        notification = notifications[0]
        # Deleting and sending the notification to the frontend as a JSON
        del notifications[0]
        return json.dumps(notification)
    return json.dumps({'type': 'NULL'})

# Employee Portal route
@app.route('/user', methods=['POST'])
def user():
    eid = int(request.form['eid'])
    return render_template("employee.html", eid=eid)

# Route for user to create new notifications for self
@app.route('/user/create', methods=['POST'])
def createSelfNotification():
    try:
        eid = int(request.form['eid'])
        # Taking all values from the HTML form
        clock = request.form['time']
        hr, mn = map(int, clock.split(':'))
        check = request.form.get('check')
        content = request.form['content']
        values = {}
        # If everyday checkbox is checked, getting number of days to notify
        if check:
            noOfDays = int(request.form['freq'])
        else: # Else, Setting number of days to 1
            noOfDays = 1
    except:
        return ERROR_MSG

    # Creating Trigger condition to store in database
    values['triggers'] = f"TM {hr} {mn} {noOfDays}"
    values['content'] = content
    values['grp'] = str(eid)
    values['type'] = "rmd"

    id = db.insert(values) # Adding notification to the database
    # starting a thread to send notification on the specified time
    # for the specified number of days (or a single day)
    threading.Thread(target=timeNotif,
                    daemon=True,
                    args=(hr, mn, noOfDays, content, id, "rmd", eid)).start()
    # Redirecting to Employee's Portal with 307 status code
    return redirect(url_for("user"), code=307)

# Route for user to suggest new notifications to admin
@app.route('/user/suggest', methods=['POST'])
def suggest():
    try:
        # Taking all values from the HTML form
        content = request.form['content']
        notitype = request.form['type']
    except:
        return ERROR_MSG
    values = {}
    values['triggers'] = "NULL"
    values['content'] = content
    values['grp'] = "ALL"
    values['type'] = notitype

    # Adding notification to the 'suggestions' table in the database
    db.insert(values, table="suggestions")
    # Redirecting to Employee's Portal with 307 status code
    return redirect(url_for("user"), code=307)

# Admin Portal Route
@app.route('/adminportal', methods=['POST'])
def admin():
    # Verifying Admin password
    if request.form['password'] == db.ADMIN_PW:
        # Retrieving notifications' suggestions from employees
        # from 'suggestions' table of the database
        try:
            suggestions = db.pending(table="suggestions")
        except:
            timer.sleep(0.5)
            suggestions = db.pending(table="suggestions")
        return render_template("admin.html", pw=db.ADMIN_PW, suggestions=suggestions)
    # Redirecting to homepage in case of wrong password
    return render_template("index.html", reg="Wrong Password")

# Route to handle actions on suggested notifications
@app.route('/adminportal/suggestion', methods=['POST'])
def handleSuggestion():
    # Getting action and suggested notification id
    task = request.form['task']
    id = int(request.form['id'])

    # If the admin decides to notify all
    if task == 'notify':
        # Getting notification content from database
        notification = db.getNoti(id, table="suggestions")[0]
        content = notification[0]
        type = notification[1]
        # Removing notifications from the database
        db.delete(id, table="suggestions")
        # Creating and starting a thread to send notification to everyone
        threading.Thread(target=notifyAll,
                        daemon=True,
                        args=(content, type)).start()
        timer.sleep(0.1)

    # If the admin decides to discrad suggestion
    elif task == 'discard':
        # Removing notifications from the database
        db.delete(id, table="suggestions")

    # Redirecting to the Admin Portal with 307 status code
    return redirect(url_for("admin"), code=307)


# Route to handle API calls
@app.route('/api', methods=['POST'])
def api():
    try:
        # If API call is to add score to an employee
        if request.json['Header'] == 'Score':
            # Parsing Employee_id and score to be added from the recieved JSON
            score = request.json['Score']
            eid = request.json['Employee_id']
            # Adding score to the Employee
            db.addScore(eid, score)
            return "Score has been added to employee"

        # If API call is to pass monthly achievement an employee
        elif request.json['Header'] == 'Monthly Achievement':
            # Parsing Employee_id and monthly achievement from the recieved JSON
            percent = request.json['Achievement %']
            eid = request.json['Employee_id']
            # Creating and starting a thread to notify accordingly
            threading.Thread(target=MonthlyAchievementNotif,
                            daemon=True,
                            args=(eid, percent)).start()
            return """Monthly achievement of the employee has been added
                    and the employee will been notified accordingly
                    if the trigger for the same has been set"""
        
        # If API call is to mark activity for an user today
        elif request.json['Header'] == 'Activity Status':
            # Parsing Employee_id from the recieved JSON
            eid = request.json['Employee_id']
            if request.json['Status'] == "Active":
                # Adding activity of the employee
                db.addActivity(eid)
                return "User's Activity point has been added for today"
            elif request.json['Status'] == "Inactive":
                # Resetting activity of the employee
                db.addActivity(eid, reset=True)
                return "User has been marked inactive for today"

        # If API call is to signup a new employee
        elif request.json['Header'] == 'Signup':
            # Parsing all values from the recieved JSON
            grp = request.json['Position']
            if grp == 'Manager':
                grp = 'MNG'
            elif grp == 'CEO':
                pass
            elif grp == 'Staff':
                grp = 'STF'
            elif grp == 'Team Leader':
                grp = 'TML'
            else:
                grp = 'OTH'
            values = {
            'name': request.json['Name'],
            'eid': request.json['Employee_id'],
            'sex': request.json['Sex'],
            'age': request.json['Age'],
            'email': request.json['Email'],
            'phone': request.json['Phone'],
            'grp': grp
            }
            # Adding new Employee to the database
            db.newUser(values)
            return "New Employee has been added"
        return "Invalid json header"
    except:
        return "Invalid type of data fed"


# Route to handle new notifications' creation by admin
@app.route('/adminportal/create/<type>', methods=['POST'])
def create(type):
    # If creating new trigger for monthly achievement
    if type == 'monthachievement':
        try:
            # Deleting any existing trigger condition for same type
            id = db.pending(trig="MA")[0][0]
            db.delete(id)
        except:
            pass
        finally:
            try:
                # Getting minimum and optimum values as inputed
                minn = int(request.form['minachieve'])
                opt = int(request.form['optachieve'])
                values = {
                    'content': "NULL",
                    'grp': "ALL",
                    'type': "",
                    'triggers': f"MA {minn} {opt}"
                }
                # Adding trigger to the database
                db.insert(values)
            except:
                return ERROR_MSG

    # If creating new trigger for daily, weekly or monthly scores
    elif type == 'score':
        # Checking if trigger is for daily, weekly or monthly scores
        x = request.form['freq']
        if x == 'daily':
            x = 'SD'
        elif x == 'weekly':
            x = 'SW'
        elif x == 'monthly':
            x = 'SM'
        try:
            # Deleting any existing trigger condition for same type
            id = db.pending(trig=x)[0][0]
            db.delete(id)
        except:
            pass
        finally:
            try:
                # Getting minimum and optimum values as inputed
                minn = int(request.form['minscore'])
                opt = int(request.form['optscore'])
                values = {
                    'content': "NULL",
                    'grp': "ALL",
                    'type': "",
                    'triggers': f"{x} {minn} {opt}"
                }
                # Adding trigger to the database
                db.insert(values)
            except:
                return ERROR_MSG

    # If creating trigger for User's inactivity
    elif type == 'inactivity':
        try:
            # Deleting any existing trigger condition for same type
            id = db.pending(trig="IA")[0][0]
            db.delete(id)
        except:
            pass
        finally:
            try:
                # Getting input data from the HTML form
                clock = request.form['time']
                hr, mn = map(int, clock.split(':'))
                freq = int(request.form['frequency'])
            except:
                return ERROR_MSG
            
            # Creating Trigger condition to store in database
            values = {
                'content': "NULL",
                'grp': "ALL",
                'type': "alr",
                'triggers': f"IA {hr} {mn} {freq}"
            }
            id = db.insert(values) # Adding notification to the database
            global statusNotifThreadActive
            if not statusNotifThreadActive:
                # Setting a flag to check that the Inactivity alert thread is active
                statusNotifThreadActive = True
                # starting a thread to send inactivity alert on the specified time
                threading.Thread(target=statusNotifThread,
                                daemon=True).start()
                timer.sleep(0.1)

    # If creating new time-based notification
    elif type == 'time':
        try:
            # Getting input data from the HTML form
            clock = request.form['time']
            hr, mn = map(int, clock.split(':'))
            check = request.form.get('check')
            content = request.form['content']
            notitype = request.form['type']
            values = {}
            # If everyday checkbox is checked, getting number of days to notify
            if check:
                noOfDays = int(request.form['freq'])
            else: # Else, Setting number of days to 1
                noOfDays = 1
        except:
            return ERROR_MSG
        
        # Creating Trigger condition to store in database
        values['triggers'] = f"TM {hr} {mn} {noOfDays}"
        values['content'] = content
        values['grp'] = "ALL"
        values['type'] = notitype
        id = db.insert(values) # Adding notification to the database
        # starting a thread to send notifications on the specified time
        # for the specified number of days (or a single day)
        threading.Thread(target=timeNotif,
                        daemon=True,
                        args=(hr, mn, noOfDays, content, id, notitype)).start()
        timer.sleep(0.1)
        

    # If creating notification for an event
    elif type == 'event':
        try:
            # Getting input data from the HTML form
            content = request.form['content']
            days = int(request.form['days'])
            date = request.form['date']
            yr, mon, dt = map(int, date.split('-'))
            # Calculating date to send notification on
            dt, mon = timer.notifDate(dt, mon, yr, days)
            content = f"Event date: {date}\n{content}"
        except:
            return ERROR_MSG
        values = {
            'content': content,
            'grp': "ALL",
            'type': "rmd",
            'triggers': f"DT {dt} {mon}"
        }
        db.insert(values) # Adding the notification in the database

    # If creating notification for some perticular groups/role
    elif type == 'role':
        try:
            # Getting input data from the HTML form
            content = request.form['content']
            notitype = request.form['type']
            roles = request.form.getlist('roles')
        except:
            return ERROR_MSG
        
        # Creating and starting a thread to notify employees
        # belonging to the specified group(s)
        threading.Thread(target=rolesNotif,
                        daemon=True,
                        args=(content, roles, notitype)).start()
        timer.sleep(0.1)



    # Redirecting to the Admin Portal with 307 status code
    return redirect(url_for("admin"), code=307)


app.host = "localhost"
app.port = 5000

if __name__ == '__main__':
    # app.debug = True
    # Running Flask Server
    app.run()
    print("Server terminated")