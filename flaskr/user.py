from typing import Dict, Any

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from google.cloud import datastore

from gcloud import storage

from flaskr.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def show_user_profile():
    return render_template('profile.html')


@bp.route('/create-profile', methods=('GET', 'POST'))
@login_required
def show_user_profile_form():
    datastore_client = datastore.Client('protean-triode-287717')

    kind = 'user'
    name = session.get('user_id')
    if name is None:
        name = session.get('email')
    person_key = datastore_client.key(kind, name)
    persons = datastore_client.get(person_key)
    if persons is not None:
        fullname = persons['fullname']
        address = persons['address']
        phone = persons['phone']
        skills = persons['skills']
        education = persons['education']
        certifications = persons['certifications']
        return render_template('add-profile.html', fullname=fullname, address=address, phone=phone, skills=skills,
                               education=education, certifications=certifications)

    return render_template('add-profile.html', name="", address="", phone="", skills="", education="",
                           certifications="")


@bp.route('/create', methods=('POST', 'GET'))
@login_required
def create_user():
    fullname = request.form['fullname']
    phone = request.form['phone']
    address = request.form['address']
    skills = request.form['skills']
    education = request.form['education']
    certifications = request.form['certifications']
    file = request.files['photo']
    datastore_client = datastore.Client('protean-triode-287717')
    client = storage.Client(project='protean-triode-287717')
    bucket = client.get_bucket('protean-triode-287717.appspot.com')
    file.filename = str(phone)+".jpg"
    blob = bucket.blob(file)
    blob.upload_from_file(file)
    kind = 'user'
    name = session.get('user_id')
    if name is None:
        name = session.get('email')
    person_key = datastore_client.key(kind, name)
    person = datastore.Entity(key=person_key)
    person['address'] = address
    person['phone'] = phone
    person['skills'] = skills
    person['education'] = education
    person['certifications'] = certifications
    person['fullname'] = fullname

    datastore_client.put(person)

    return redirect(url_for('user.show_user_profile'))


@bp.route('/view', methods=('POST', 'GET'))
@login_required
def view_user():
    datastore_client = datastore.Client('protean-triode-287717')

    kind = 'user'
    name = session.get('user_id')
    if name is None:
        name = session.get('email')
    person_key = datastore_client.key(kind, name)
    persons = datastore_client.get(person_key)
    if persons is None:
        return redirect(url_for('user.show_user_profile_form'))

    user_dict = {
        'Full Name': persons['fullname'],
        'Address': persons['address'],
        'Phone': persons['phone'],
        'Skills': persons['skills'],
        'Education': persons['education'],
        'Certifications': persons['certifications'],
    }

    return render_template("view.html", user=user_dict)
