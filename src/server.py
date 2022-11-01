from flask import Flask, render_template
app = Flask(__name__)

@app.route('/api/')
def homepage():
    return render_template('index.html')

@app.route('/api/v1/')
def versions():
    return render_template('versions.html')

@app.route('/api/v1/jobs')
def available_jobs():
    return render_template('apiview.html')
    