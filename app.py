"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Blogly

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def index():
    """This is just the form"""
    
    return redirect("/users/new")

@app.route("/users/new", methods=["GET"])
def newform():
    blogly = Blogly.query.all()
    """shows list of all names in db"""
    return render_template("new.html", blogly = blogly)


@app.route("/users/new", methods=["POST"])
def getusers():  
    # this adds the new user into the database
    new_user = Blogly(
        first_name = request.form["first"],
        last_name = request.form["last"],
        image_url = request.form["image"])
    
     # this will commit and add it to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users", methods=["GET"])
def list():
    blogly = Blogly.query.all()
    """shows list of all names in db"""
    return render_template("users.html", blogly = blogly)


@app.route("/users/<int:blogly_id>")
def details(blogly_id):
    fname = Blogly.query.get(blogly_id).first_name
    lname = Blogly.query.get(blogly_id).last_name
    imgsrc = Blogly.query.get(blogly_id).image_url
    return render_template("details.html" ,blogly_id = blogly_id, fname = fname, lname = lname, imgsrc = imgsrc)

2
@app.route('/users/<int:blogly_id>/edit', methods=["GET"])
def users_edit(blogly_id):
    """Show a form to edit an existing user"""

    user = Blogly.query.get_or_404(blogly_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:blogly_id>/edit', methods=["POST"])
def users_update(blogly_id):
    """Handle form submission for updating an existing user"""

    user = Blogly.query.get_or_404(blogly_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:blogly_id>/delete', methods=["POST"])
def users_destroy(blogly_id):
    """Handle form submission for deleting an existing user"""

    user = Blogly.query.get_or_404(blogly_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

