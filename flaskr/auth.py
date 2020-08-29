import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_database_connection, close_database_connection

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        connection = get_database_connection()
        db = connection.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        db.execute(
            'SELECT id FROM user WHERE username = %s', (username,)
        )

        if db.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            hashed_password = generate_password_hash(password)
            db.execute(
                'INSERT INTO user (username, password) VALUES (%s, %s)',
                (username, hashed_password)
            )
            connection.commit()
            db.close()
            close_database_connection(connection)
            return redirect(url_for('auth.login'))
        connection.commit()
        db.close()
        close_database_connection(connection)
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        connection = get_database_connection()
        db = connection.cursor()
        error = None
        db.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )

        user = db.fetchone()
        if not user:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[1]
            return redirect(url_for('user.show_user_profile'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    user_email = session.get('email')
    if user_email is not None:
        g.user = user_email
    else:
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM user WHERE username = %s', (user_id,)
            )
            g.user = cursor.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
