from flask import Flask, render_template, request, redirect, url_for
import db
import threading
import timer
import bots.mail
import bots.sms

def notifyThread(email, phone, content, type, sub):
    bots.mail.sendMail(email, sub, content)
    bots.sms.sendMsg(phone, content)

def notify(email, phone, content, type, sub=db.SUBJECT):
    if type == "":
        type = "rmd"
    threading.Thread(target=notifyThread,
                    daemon=True,
                    args=(email, phone, content, type, sub)).start()



def dayThread():
    while True:
        timer.startDay()
        try:
            notification = db.pending(trig="SD")[0]
        except:
            return
        _, minn, opt = notification[4].split()
        users = db.getUsers()
        for user in users:
            email, phone = user[1], user[2]
            score = user[3]
            if score < int(minn):
                notify(email, phone, db.SCORE_DAY_LEV1, 'alr')
            elif score < int(opt):
                notify(email, phone, db.SCORE_DAY_LEV2, 'rmd')
            else:
                notify(email, phone, db.SCORE_DAY_LEV3, 'rwd')
        db.resetScore()

        notifications = db.pending(trig="DT")
        for notification in notifications:
            _, dt, mn = notification[4].split()
            dt, mn = int(dt), int(mn)
            date, month = timer.curDate(onlydm=True)
            if dt == date and mn == month:
                content = notification[1]
                id = notification[0]
                for user in users:
                    email, phone = user[1], user[2]
                    notify(email, phone, content, "rmd")
                db.delete(id)
        timer.time.sleep(2)

def weekThread():
    while True:
        timer.startWeek()
        try:
            notification = db.pending(trig="SW")[0]
        except:
            return
        _, minn, opt = notification[4].split()
        for user in db.getUsers():
            email, phone = user[1], user[2]
            score = user[4]
            if score < int(minn):
                notify(email, phone, db.SCORE_WEEK_LEV1, 'alr')
            elif score < int(opt):
                notify(email, phone, db.SCORE_WEEK_LEV2, 'rmd')
            else:
                notify(email, phone, db.SCORE_WEEK_LEV3, 'rwd')
        db.resetScore(week=True)
        timer.time.sleep(2)

def monthThread():
    while True:
        timer.startMonth()
        try:
            notification = db.pending(trig="SM")[0]
        except:
            return
        _, minn, opt = notification[4].split()
        for user in db.getUsers():
            email, phone = user[1], user[2]
            score = user[5]
            if score < int(minn):
                notify(email, phone, db.SCORE_MONTH_LEV1, 'alr')
            elif score < int(opt):
                notify(email, phone, db.SCORE_MONTH_LEV2, 'rmd')
            else:
                notify(email, phone, db.SCORE_MONTH_LEV3, 'rwd')
        db.resetScore(month=True)
        timer.time.sleep(2)



threading.Thread(target=dayThread, daemon=True).start()
threading.Thread(target=weekThread, daemon=True).start()
threading.Thread(target=monthThread, daemon=True).start()


def MonthlyAchievementNotif(eid, percent):
    try:
        notification = db.pending(trig="MA")[0]
    except:
        return
    user = db.getUsers(eid)[0]
    email, phone = user[1], user[2]
    _, minn, opt = notification[4].split()
    if percent < int(minn):
        notify(email, phone, db.ACHIEVE_LEV1, 'alr')
    elif percent < int(opt):
        notify(email, phone, db.ACHIEVE_LEV2, 'rmd')
    else:
        notify(email, phone, db.ACHIEVE_LEV3, 'rwd')

def timeNotif(hr, mn, freq, content, id, type='rmd', eid=False):
    while freq > 0:
        timer.afterTime(hr, mn)
        if eid:
            user = db.getUsers(eid)[0]
            email, phone = user[1], user[2]
            notify(email, phone, content, type)
        else:
            for user in db.getUsers():
                email, phone = user[1], user[2]
                notify(email, phone, content, type)

        newTrig = f"TM {hr} {mn} {freq-1}"
        db.changeTrigger(id, newTrig)
        freq -= 1
        timer.time.sleep(2)
    db.delete(id)

def rolesNotif(content, roles, type='rmd'):
    users = db.getUsers()
    for user in users:
        if user[0] in roles:
            email, phone = user[1], user[2]
            notify(email, phone, content, type)

def notifyAll(content, type):
    for user in db.getUsers():
        email, phone = user[1], user[2]
        notify(email, phone, content, type)

notifications = db.pending(trig="TM")
for notification in notifications:
    _, hr, mn, freq = notification[4].split()
    id = notification[0]
    hr, mn, freq = int(hr), int(mn), int(freq)
    content = notification[1]
    type = notification[2]
    grp = notification[3]
    if grp == "ALL":
        eid = False
    else:
        eid = int(grp)
    threading.Thread(target=timeNotif,
                        daemon=True,
                        args=(hr, mn, freq, content, id, type, eid)).start()



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        values = {
            'name': request.form['name'],
            'eid': int(request.form['eid']),
            'sex': request.form['sex'],
            'age': int(request.form['age']),
            'email': request.form['email'],
            'phone': request.form['phone'],
            'grp': request.form['group']
        }
        db.newUser(values)
        return render_template("index.html", reg="User Added")
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/user', methods=['POST'])
def user():
    eid = int(request.form['eid'])
    return render_template("employee.html", eid=eid)

@app.route('/user/create', methods=['POST'])
def createSelfNotification():
    eid = int(request.form['eid'])
    clock = request.form['time']
    hr, mn = map(int, clock.split(':'))
    check = request.form.get('check')
    content = request.form['content']
    values = {}
    if check:
        noOfDays = int(request.form['freq'])
    else:
        noOfDays = 1
    values['triggers'] = f"TM {hr} {mn} {noOfDays}"
    values['content'] = content
    values['grp'] = str(eid)
    values['type'] = "rmd"
    id = db.insert(values)
    threading.Thread(target=timeNotif,
                    daemon=True,
                    args=(hr, mn, noOfDays, content, id, "rmd", eid)).start()
    return redirect(url_for("user"), code=307)

@app.route('/user/suggest', methods=['POST'])
def suggest():
    content = request.form['content']
    notitype = request.form['type']
    values = {}
    values['triggers'] = "NULL"
    values['content'] = content
    values['grp'] = "ALL"
    values['type'] = notitype
    db.insert(values, table="suggestions")
    return redirect(url_for("user"), code=307)


@app.route('/adminportal', methods=['POST'])
def admin():
    if request.form['password'] == db.ADMIN_PW:
        suggestions = db.pending(table="suggestions")
        return render_template("admin.html", pw=db.ADMIN_PW, suggestions=suggestions)
    return render_template("index.html", reg="Wrong Password")

@app.route('/adminportal/suggestion', methods=['POST'])
def handleSuggestion():
    task = request.form['task']
    id = int(request.form['id'])
    if task == 'notify':
        notification = db.getNoti(id, table="suggestions")[0]
        content = notification[0]
        type = notification[1]
        db.delete(id, table="suggestions")
        threading.Thread(target=notifyAll,
                        daemon=True,
                        args=(content, type)).start()
    elif task == 'discard':
        db.delete(id, table="suggestions")
    return redirect(url_for("admin"), code=307)

@app.route('/api', methods=['POST'])
def api():
    try:
        if request.json['Header'] == 'Score':
            score = request.json['Score']
            eid = request.json['Employee_id']
            db.addScore(eid, score)
            return "Score has been added to employee"

        elif request.json['Header'] == 'Monthly Achievement':
            percent = request.json['Achievement %']
            eid = request.json['Employee_id']
            threading.Thread(target=MonthlyAchievementNotif,
                            daemon=True,
                            args=(eid, percent)).start()
            return "Monthly achievement of the employee has been added"
        return "Invalid json header"
    except:
        return "Invalid data fed"

@app.route('/adminportal/create/<type>', methods=['POST'])
def create(type):
    if type == 'monthachievement':
        try:
            id = db.pending(trig="MA")[0][0]
            db.delete(id)
        except:
            pass
        finally:
            minn = request.form['minachieve']
            opt = request.form['optachieve']
            values = {
                'content': "NULL",
                'grp': "ALL",
                'type': "",
                'triggers': f"MA {minn} {opt}"
            }
            db.insert(values)

    elif type == 'score':
        x = request.form['freq']
        if x == 'daily':
            x = 'SD'
        elif x == 'weekly':
            x = 'SW'
        elif x == 'monthly':
            x = 'SM'
        try:
            id = db.pending(trig=x)[0][0]
            db.delete(id)
        except:
            pass
        finally:
            minn = request.form['minscore']
            opt = request.form['optscore']
            values = {
                'content': "NULL",
                'grp': "ALL",
                'type': "",
                'triggers': f"{x} {minn} {opt}"
            }
            db.insert(values)

    elif type == 'time':
        clock = request.form['time']
        hr, mn = map(int, clock.split(':'))
        check = request.form.get('check')
        content = request.form['content']
        notitype = request.form['type']
        values = {}
        if check:
            noOfDays = int(request.form['freq'])
        else:
            noOfDays = 1
        values['triggers'] = f"TM {hr} {mn} {noOfDays}"
        values['content'] = content
        values['grp'] = "ALL"
        values['type'] = notitype
        id = db.insert(values)
        threading.Thread(target=timeNotif,
                        daemon=True,
                        args=(hr, mn, noOfDays, content, id, notitype)).start()

    elif type == 'event':
        content = request.form['content']
        days = int(request.form['days'])
        date = request.form['date']
        yr, mon, dt = map(int, date.split('-'))
        dt, mon = timer.notifDate(dt, mon, yr, days)
        content = f"Event date: {date}\n{content}"
        values = {
            'content': content,
            'grp': "ALL",
            'type': "rmd",
            'triggers': f"DT {dt} {mon}"
        }
        db.insert(values)

    elif type == 'role':
        content = request.form['content']
        notitype = request.form['type']
        roles = request.form.getlist('roles')
        threading.Thread(target=rolesNotif,
                        daemon=True,
                        args=(content, roles, notitype)).start()

        

    return redirect(url_for("admin"), code=307)

@app.route('/adminportal/create', methods=['GET','POST'])
def foo():
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run()