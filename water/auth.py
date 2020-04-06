import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from water.db import get_db

# from werkzeug.security import generate_password_hash
# import hashlib
# from random import uniform

bp = Blueprint('auth', __name__, url_prefix='/auth')

from water.logger import app


@bp.route('/register', methods=('GET', 'POST'))
def register():
    return redirect(url_for('auth.login'))

    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     db = get_db()
    #     error = None
    #
    #     if not username:
    #         error = 'Username is required.'
    #     elif not password:
    #         error = 'Password is required.'
    #     elif db.execute(
    #             'SELECT id FROM "user" WHERE username = ?', (username,)
    #     ).fetchone() is not None:
    #         error = 'User {} is already registered.'.format(username)
    #
    #     if not error:
    #         token = hashlib.sha1('{}|{}'.format(username, uniform(1, 99999))
    #         db.execute(
    #             'INSERT INTO "user" (username, password, token) VALUES (?, ?, ?)',
    #             (username, generate_password_hash(password=password, salt_length=16), token)
    #         )
    #         db.commit()
    #         return redirect(url_for('auth.login'))
    #
    #     flash(error)
    #
    # return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM "user" WHERE username = ?', (username,)
        ).fetchone()

        if not user or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if not error:
            session.clear()
            session['user_id'] = user['id']
            app.logger.info('Logged in user {}'.format(user['id']))
            return redirect(url_for('index'))
        else:
            if user:
                app.logger.error('User {}'.format(user['id']))
            app.logger.error(error)

        flash(error)

    return render_template('auth/login.html')


def is_valid_authorization_string(token_string):
    if not token_string:
        return False
    token = token_string.split(' ')
    if len(token) != 2 or not token[1]:
        return False
    token = token[1]
    db = get_db()
    user = db.execute(
        'SELECT * FROM "user" WHERE token = ?', (token,)
    ).fetchone()
    return not not user


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM "user" WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
