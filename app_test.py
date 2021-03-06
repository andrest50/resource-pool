# For testing purposes

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os
import models
import templates

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "resources.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config')
app.register_error_handler(500, internal_error)
app.register_error_handler(404, not_found_error)
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def home_page():
    #models.test_db()
    print(models.User.query.all())
    return "Home Page"

@app.errorhandler(500)
def internal_error(e):
    print("500")
    #return e, 500
    return render_template('templates/500.html'), 500

@app.errorhandler(404)
def not_found_error(e):
    print("404")
    #return "Bad request", 404
    return render_template('templates/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)