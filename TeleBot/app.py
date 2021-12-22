from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_value():
    login = request.form['login']
    passwd = request.form['passwd']
    return render_template('pass.html', log=login, pswd=passwd)
