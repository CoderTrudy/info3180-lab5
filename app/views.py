"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from forms import MovieForm, form_errors
from models import db, Movie

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/submit_movie', methods=['GET', 'POST'])
def submit_movie():
    form = MovieForm()
    if form.validate_on_submit():
        # Process the form data
        title = form.title.data
        description = form.description.data
        poster = form.poster.data
        # Save the movie data, e.g., to a database
        return 'Movie submitted successfully!'
    return render_template('submit_movie.html', form=form)



###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


# Function to save uploaded file
def save_file(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

# Route to add movies
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm(request.form)
    if form.validate():
        title = form.title.data
        description = form.description.data
        poster = request.files['poster']
        poster_filename = save_file(poster)
        
        # Create new movie object
        new_movie = Movie(title=title, description=description, poster=poster_filename)
        
        # Save the movie to the database
        db.session.add(new_movie)
        db.session.commit()
        
        # Return JSON response with movie details
        return jsonify({
            "message": "Movie Successfully added",
            "title": new_movie.title,
            "poster": new_movie.poster,
            "description": new_movie.description
        }), 200
    else:
        # Return JSON response with form errors
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400



@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)