from new_user import NewUser
from log_user import LogUser
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp, template
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from db_manager import DBManager

# configure application
app = Flask(__name__)

# ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ensure responses are not cached
@app.after_request
def after_request(response):

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db manager
db = DBManager('./turitiba.db')

@app.route('/')
def index():
    '''Returns the template of the ‘/’ route. '''
    
    return render_template('index.html') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Deals with the login. If receives a request with the GET 
    method, just renders the login screen.
    Else, clears the cookies, gets the username and the password from
    the form, uses LogUser class to do error checking, writes the 
    cookies with the username if all the tests are past successfully,
    flash all the messages from the object and redirect to the correct
    route. If all is successfull, goes to the main route, if not, stays
    in the login route. 
    '''
    
    if request.method == 'GET':
        
        return render_template('login.html')
    
    session.clear()
    
    username = request.form.get('username') or ''
    password = request.form.get('password') or ''
    
    # error checking
    user = LogUser(username, password, db)
    
    if user.is_all_okay():
        session['username'] = username
        
    # flash messages
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''''
    Deals with the user registration.
    If receives a request with the GET method, just renders the register
    screen.
    If not, gets the data from the registration form, do error checking
    using the NewUser class. If all the test are past successfully, sends
    the new user data to the DB.
    Then, flashes all the messages from the object and redirects to the
    correct route. If the user is successfully registered, redirects to
    the login route, else, stays in the registration route.
    '''
    
    if request.method == 'GET':
        
        return render_template('register.html')
    
    # gets data from form
    name = request.form.get('name') or ''
    email = request.form.get('email') or ''
    username = request.form.get('username') or ''
    password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm-password') or ''
    
    # error checking
    user = NewUser(name, email, username, password, confirm_password,
                   db)
    
    if user.is_all_okay():
        user.send_to_db()
    
    # flash and redirect
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/user/<username>')
def user(username: str):
    
    return render_template('user.html')