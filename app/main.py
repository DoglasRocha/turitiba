from crypt import methods
from helpers import login_required
from new_user import NewUser
from log_user import LogUser
from update_user import UpdateUser
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp, template
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from db_manager import DBManager
from datetime import datetime
from reader import Reader

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


def update_likes_in_all_locations():
    
    for id_ in db.get_all_locations_id():
        
        update_likes_count(id_[0])
        

@app.route('/')
def index():
    '''Gets samples of the 10 most famous locations from the DB, then
    renders the template, passing the sample as argument.'''
    
    data = sample().get_json()
    
    return render_template('index.html', sample=data) 


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
@login_required
def user(username: str):
    
    user_info = Reader.get_user_info(db, username)
    
    return render_template('user.html', info=user_info)


@app.route('/update-user/<username>', methods=['POST'])
@login_required
def update_user(username):
    
    name = request.form.get('name') or ''
    email = request.form.get('email') or ''
    current_password = request.form.get('old-password') or ''
    new_password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm-password') or ''
    
    # error checking
    user = UpdateUser(name, email, username, current_password,
                      new_password, confirm_password, db)
    
    if user.is_all_okay():
        user.update_user_in_db()
        
    # flash messages
    for message in user.get_messages():
        flash(message)
        
    return redirect(user.get_redirection())


@app.route('/sample')
def sample():
    
    update_likes_in_all_locations()
    
    sample = Reader.get_sample_locations_sample(db, 10)
        
    return jsonify(sample)


@app.route('/location/<location_name>')
def location(location_name: str):
        
    data = location_data(location_name).get_json()
    has_liked = user_has_liked(session.get('username'), location_name)
    
    return render_template('location.html', data=data, user_has_liked=has_liked)


@app.route('/location-data/<location_route>')
def location_data(location_route: str):
    
    data = Reader.get_location_data(db, location_route)
    
    return jsonify(data)


def user_has_liked(username: str, location_route: str) -> bool:
    
    if not (username):
        return False
    
    return Reader.user_has_liked(db, username, location_route)


@app.route('/logout', methods=['POST'])
def logout():
    
    callback = request.args.get('callback')
    session.clear()
    flash('Deslogado com sucesso!')
    
    return redirect(f'/{callback}')
    
    
@app.route('/main')
def main():
    
    return redirect('/')


@app.route('/manage-likes/<location_route>', methods=['POST'])
@login_required
def manage_likes(location_route: str) -> str:
    
    user_id = Reader.get_user_id(db, session['username'])
    location_id = Reader.get_location_id(db, location_route)
    
    user_has_register = Reader.user_has_register_in_likes_table(
        db, session['username'], location_route
    )
    
    if not (user_has_register):
        
        insert_like(user_id, location_id)
        update_likes_count(location_id)
        return ''
        
        
    has_liked = Reader.user_has_liked(
        db, session['username'], location_route
    )
    
    if (has_liked):
    
        unlike_location(user_id, location_id)
        update_likes_count(location_id)
        return ''
    
    
    like_location(user_id, location_id)
    update_likes_count(location_id)
    return ''
        


def unlike_location(user_id: int, location_id: int) -> None:
    
    db.unlike_location(user_id, location_id)
    

def like_location(user_id: int, location_id: int) -> None:
    
    db.like_location(user_id, location_id)
    

def insert_like(user_id: str, location_id: int) -> None:
    
    db.insert_like_in_location(user_id, location_id)
    
    
def update_likes_count(location_id: int) -> None:
    
    likes_count = Reader.get_likes_in_location(db, location_id)
    
    db.update_likes_in_location(location_id, likes_count)


@app.route('/get-likes/<location_route>')
def get_likes_from_location(location_route: str) -> int:
    
    location_id = Reader.get_location_id(db, location_route)
    likes = Reader.get_likes_in_location(db, location_id)
    
    return jsonify({'likes': likes})


@app.route('/comment/<location_route>', methods=['POST'])
@login_required
def comment(location_route: str) -> None:
    
    redirect_route = f'/location/{location_route}'
    user_comment = request.form.get('comment')
    user_id = Reader.get_user_id(db, session['username'])
    location_id = Reader.get_location_id(db, location_route)
    date = datetime.now()
    
    db.insert_comment_in_location(
        user_comment, 
        user_id, 
        location_id, 
        date
    )
    
    return redirect(redirect_route)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return f'Name: {e.name}, code: {e.code}'
    

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    