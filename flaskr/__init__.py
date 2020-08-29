from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, url_for, redirect, session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id='492292518404-mtu13d1u3gfqigia5p0dct0rlo5l57t6.apps.googleusercontent.com',
        client_secret='FY2p6j6D8g7ppkg3q8eFtsdy',
        project_id="protean-triode-287717",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        access_token_params=None,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1",
        client_kwargs={'scope': 'openid profile email'},
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    )

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route('/oauth/login')
    def login():
        google = oauth.create_client('google')
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route('/authorize')
    def authorize():
        google = oauth.create_client('google')  # create the google oauth client
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scope
        user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
        session['email'] = user.get('email')
        return redirect(url_for('user.show_user_profile'))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)

    return app
