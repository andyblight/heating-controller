from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    sensors = [
        {
            'name': 'External',
            'temperature': '30',
            'humidity': '90'
        },
        {
            'name': 'Upstairs',
            'temperature': '27',
            'humidity': '70'
        },
        {
            'name': 'Downstairs',
            'temperature': '20',
            'humidity': '50'
        }
    ]
    return render_template('index.html', title='Home', sensors=sensors)
