from flask import Flask
from config import Config
from flask_googlecharts import GoogleCharts

app = Flask(__name__)
app.config.from_object(Config)
charts = GoogleCharts(app)


from app import routes  # noqa: 401
