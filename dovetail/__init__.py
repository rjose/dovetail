from flask import Flask, render_template, request, redirect, url_for, g
from datetime import datetime

import dovetail.database as database

import dovetail.projects.controller
import dovetail.people.controller
import dovetail.work.controller
import os
from werkzeug.wsgi import SharedDataMiddleware

database.metadata.create_all()

app = Flask(__name__)

@app.before_request
def open_connection():
    g.connection = database.engine.connect()

@app.teardown_request
def close_connection(exeption=None):
    g.connection.close()


@app.route('/')
def root():
    return redirect('/projects')

@app.route('/home')
def root():
    return render_template('home/index.html')

# Static files


# Register blueprints
app.register_blueprint(dovetail.people.controller.mod)
app.register_blueprint(dovetail.projects.controller.mod)
app.register_blueprint(dovetail.work.controller.mod)

# Register middleware
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/assets': os.path.join(os.path.dirname(__file__), 'assets')})

if __name__ == '__main__':
    # TODO: Figure out how to set this via an environment variable
    app.run(debug=True)

