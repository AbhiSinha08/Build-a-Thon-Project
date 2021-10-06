from flask import Flask, render_template, redirect, request
import db

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> Index </h1>"

if __name__ == '__main__':
    app.run()