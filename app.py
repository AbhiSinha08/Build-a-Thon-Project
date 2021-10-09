from flask import Flask, render_template, redirect, request, jsonify
import db

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

@app.route('/adminportal', methods=['POST'])
def admin():
    if request.form['password'] == db.adminPW:
        return render_template("admin.html")
    return render_template("index.html", reg="Wrong Password")

if __name__ == '__main__':
    app.run()