from flask import Flask, render_template, request, redirect, url_for
import db
import threading
import timer
import bots.mail
import bots.telegram

app = Flask(__name__)

threading.Thread(target=timer.startDay, daemon=True).start()
threading.Thread(target=timer.startMonth, daemon=True).start()
threading.Thread(target=timer.startWeek, daemon=True).start()

def notify(email, phone, content, type, sub="Auto-Generated Notification"):
    if type == "":
        type = "rmd"
    bots.mail.sendMail(email, sub, content)
    bots.telegram.sendMsg(phone, content)


def MonthlyAchievementNotis(eid, percent):
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

def timeNotif(hr, mn, freq, content, id, type='rmd'):
    while freq > 0:
        timer.afterTime(hr, mn)
        users = db.getUsers()
        for user in users:
            email, phone = user[1], user[2]
            notify(email, phone, content, type)

        newTrig = f"TM {hr} {mn} {freq-1}"
        db.changeTrigger(id, newTrig)
        freq -= 1
        timer.time.sleep(2)
    db.delete(id)



notifications = db.pending(trig="TM")
for notification in notifications:
    _, hr, mn, freq = notification[4].split()
    id = notification[0]
    hr, mn, freq = int(hr), int(mn), int(freq)
    content = notification[1]
    type = notification[2]
    threading.Thread(target=timeNotif,
                        daemon=True,
                        args=(hr, mn, freq, content, id, type)).start()



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

@app.route('/adminportal', methods=['POST'])
def admin():
    if request.form['password'] == db.ADMIN_PW:
        return render_template("admin.html", pw=db.ADMIN_PW)
    return render_template("index.html", reg="Wrong Password")

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
            db.addAchievement(eid, percent)
            threading.Thread(target=MonthlyAchievementNotis,
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
        values = {
            'content': content,
            'grp': "ALL",
            'type': "rmd",
            'triggers': f"DT {dt} {mon}"
        }
        db.insert(values)

    return redirect(url_for("admin"), code=307)

@app.route('/adminportal/create', methods=['GET','POST'])
def foo():
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run()