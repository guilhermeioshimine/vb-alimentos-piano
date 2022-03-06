from logging import DEBUG, debug
from flask import Flask
from routes.report import *


app = Flask(__name__)
app.debug = True

app.register_blueprint(report_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0' )